import argparse
from typing import Dict, List, Tuple, Any
from src.engine.core import Engine
from src.engine.optimizer import (
    calculate_units, calculate_cost, find_best_path, get_effects_value
)


def fmt_choices(items):
    """Format a list of items as choices for command-line help."""
    return " | ".join(f"{i+1}={item}" for i, item in enumerate(items))


class CapitalizationHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter that capitalizes help text and improves formatting."""
    
    def __init__(self, prog):
        super().__init__(prog, max_help_position=40, width=80)
        
    def _format_action(self, action):
        if action.help and not action.help[0].isupper():
            action.help = action.help[0].upper() + action.help[1:]
        return super()._format_action(action)
        
    def _join_parts(self, part_strings):
        for i, part in enumerate(part_strings):
            if part.startswith('usage:'):
                part_strings[i] = 'Usage:' + part[6:]
            elif part.startswith('positional arguments'):
                part_strings[i] = 'Positional Arguments:\n' + part.split('\n', 1)[1]
            elif part.startswith('options'):
                part_strings[i] = 'Options:\n' + part.split('\n', 1)[1]
        return super()._join_parts(part_strings)


def setup_optimizer_parser(subparsers):
    """Set up the command-line parser for the optimizer mode.
    
    Args:
        subparsers: Subparsers object from the main parser
        
    Returns:
        The created subparser for the optimizer mode
    """
    # Create the optimizer subparser
    parser = subparsers.add_parser(
        '2', 
        help='Find the most profitable drug recipe',
        description='Drug Optimizer - Find the most profitable combination of ingredients',
        formatter_class=CapitalizationHelpFormatter
    )
    
    # Add drug type as a flag
    parser.add_argument('-t', '--type', type=int, required=True, metavar='N',
                        help='Drug type (1=marijuana, 2=meth, 3=cocaine)')
    
    # Production options
    prod = parser.add_argument_group('Production')
    prod.add_argument('-d', '--depth', type=int, default=3, metavar='N',
                      help='Search depth (default: 3)')
    prod.add_argument('-g', '--grow-tent', action='store_true', 
                      help='Use grow tent')
    prod.add_argument('-p', '--pgr', action='store_true', 
                      help='Use plant growth regulators')
    
    # Marijuana options
    m_opts = parser.add_argument_group('Marijuana')
    m_opts.add_argument('-s', '--strain', type=int, default=1, metavar='N',
                        help='Strain (1=og_kush, 2=sour_diesel, etc.)')
    
    # Meth options
    me_opts = parser.add_argument_group('Meth')
    me_opts.add_argument('-q', '--quality', type=int, choices=range(1, 4),
                         default=3, help='Quality: 1=low | 2=medium | 3=high (default: 3)')
    
    return parser


def setup_marijuana_options(args, data: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
    """Set up marijuana-specific options for optimization.
    
    Args:
        args: Command-line arguments
        data: Dictionary containing all loaded data
        
    Returns:
        Tuple containing:
        - List of initial effects
        - Dictionary of options for cost calculation
    """
    # Get strain information
    strain_index = args.strain - 1
    strains = list(data['strain_data'].keys())
    strain = strains[strain_index]
    
    # Get initial effect from strain
    initial_effects = [data['strain_data'][strain][0]]
    
    # Set up options for cost calculation
    options = {
        'strain': strain,
        'grow_tent': args.grow_tent,
        'pgr': args.pgr
    }
    
    return initial_effects, options


def setup_meth_options(args, data: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
    """Set up meth-specific options for optimization.
    
    Args:
        args: Command-line arguments
        data: Dictionary containing all loaded data
        
    Returns:
        Tuple containing:
        - List of initial effects (empty for meth)
        - Dictionary of options for cost calculation
    """
    # Meth has no initial effects
    initial_effects = []
    
    # Set up options for cost calculation
    options = {
        'quality': args.quality,
        'grow_tent': args.grow_tent,
        'pgr': args.pgr
    }
    
    return initial_effects, options


def setup_cocaine_options(args, data: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
    """Set up cocaine-specific options for optimization.
    
    Args:
        args: Command-line arguments
        data: Dictionary containing all loaded data
        
    Returns:
        Tuple containing:
        - List of initial effects (empty for cocaine)
        - Dictionary of options for cost calculation
    """
    # Cocaine has no initial effects
    initial_effects = []
    
    # Set up options for cost calculation
    options = {
        'grow_tent': args.grow_tent,
        'pgr': args.pgr
    }
    
    return initial_effects, options


def calculate_drug_cost(drug_type: str, options: Dict[str, Any], data: Dict[str, Any]) -> float:
    """Calculate the production cost for a drug.
    
    Args:
        drug_type: Type of drug being produced
        options: Dictionary of options for cost calculation
        data: Dictionary containing all loaded data
        
    Returns:
        Production cost per unit
    """
    # Get common parameters
    constants = data['drug_pricing']['constants']
    cost_formula = data['drug_pricing']['cost_calculations'][drug_type]['formula']
    
    # Calculate units based on grow tent and pgr options
    units = calculate_units(
        drug_type, 
        options.get('grow_tent', False), 
        options.get('pgr', False), 
        data['drug_pricing']['production_units']
    )
    
    # Set up keyword arguments based on drug type
    kwargs = {'units': units}
    
    if drug_type == 'marijuana':
        kwargs.update({
            'strain': options.get('strain', 'og_kush'),
            'strain_data': data['strain_data']
        })
    elif drug_type == 'meth':
        kwargs.update({
            'quality': options.get('quality', 3),
            'quality_costs': data['quality_costs']
        })
    elif drug_type == 'cocaine':
        kwargs.update({
            'ingredient_prices': data['ingredient_prices']
        })
    
    # Calculate the production cost
    return calculate_cost(drug_type, constants, cost_formula, **kwargs)


def print_optimization_results(drug_type: str, effects: List[str], path: List[str], 
                              ingredient_cost: float, prod_cost: float, base_price: float,
                              effect_multipliers: Dict[str, float]) -> None:
    """Print the results of the optimization.
    
    Args:
        drug_type: Type of drug being produced
        effects: List of effects in the optimal combination
        path: List of ingredients in the optimal combination
        ingredient_cost: Cost of the ingredients
        prod_cost: Production cost per unit
        base_price: Base price of the drug
        effect_multipliers: Dictionary mapping effects to their value multipliers
    """
    from src.engine.optimizer import get_effects_value
    
    # Calculate value and profit
    total_value = get_effects_value(effects, base_price, effect_multipliers)
    total_cost = prod_cost + ingredient_cost
    profit = total_value - total_cost
    
    # Print the results
    print(f"\nBest Combination for {drug_type}:")
    print(f"Production Cost: ${prod_cost:.2f}")
    print(f"Ingredients: {', '.join(path)}")
    print(f"Ingredient Cost: ${ingredient_cost:.2f}")
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Total Value: ${total_value:.2f}")
    print(f"Profit: ${profit:.2f}")
    print(f"Effects: {', '.join(effects)}")
    print(f"Recipe: {' → '.join(path)}")


def run_optimizer(args, data: Dict[str, Any]) -> None:
    """Run the optimizer with the given arguments.
    
    Args:
        args: Command-line arguments
        data: Dictionary containing all loaded data
    """
    # Map numeric drug type to string
    drug_types = data['drug_types']
    drug_type = drug_types[args.type - 1]
    
    # Set up drug-specific options
    if drug_type == 'marijuana':
        initial_effects, options = setup_marijuana_options(args, data)
    elif drug_type == 'meth':
        initial_effects, options = setup_meth_options(args, data)
    else:  # cocaine
        initial_effects, options = setup_cocaine_options(args, data)
    
    # Calculate production cost
    prod_cost = calculate_drug_cost(drug_type, options, data)
    
    # Get base price for the drug
    base_price = data['drug_pricing']['base_prices'][drug_type]
    
    # Create engine
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    
    # Find the best path
    result = find_best_path(
        engine, base_price, prod_cost, args.depth,
        data['effect_multipliers'], data['ingredient_prices'], data['effect_priorities'],
        initial_effects
    )
    
    if result:
        effects, path, ingredient_cost = result
        print_optimization_results(
            drug_type, effects, path, ingredient_cost, 
            prod_cost, base_price, data['effect_multipliers']
        )
    else:
        print(f"No profitable combination found for {drug_type} with depth {args.depth}")
