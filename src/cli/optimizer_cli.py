import argparse
from typing import Dict, List, Tuple, Any
from src.engine.core import Engine
from src.engine.optimizer.core import (
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


def setup_optimizer_parser(parser):
    """Set up the command-line parser for the optimizer mode.
    
    Args:
        parser: The main argument parser
        
    Returns:
        The updated parser with optimizer arguments
    """
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


def run_optimizer(args, data):
    """Run the optimizer with the given arguments and data.
    
    Args:
        args: Parsed command-line arguments
        data: Dictionary containing all loaded data
        
    Returns:
        None, prints results to stdout
    """
    # Extract data
    max_effects = data['max_effects']
    effect_priorities = data['effect_priorities']
    rules_data = data['combinations']
    effect_multipliers = data['effect_multipliers']
    ingredient_prices = data['ingredient_prices']
    drug_types = data['drug_types']
    strain_data = data['strain_data']
    quality_names = data['quality_names']
    quality_costs = data['quality_costs']
    drug_pricing = data['drug_pricing']
    
    # Validate drug type
    if args.type < 1 or args.type > len(drug_types):
        print(f"Error: Invalid drug type. Must be between 1 and {len(drug_types)}")
        return
    
    # Process drug type and prepare configuration
    drug_type = drug_types[args.type - 1]
    base_price = drug_pricing['base_prices'][drug_type]
    constants = drug_pricing['constants']
    cost_formula = drug_pricing['cost_calculations'].get(drug_type, {}).get('formula', '')
    prod_cost, display, effects = 0, '', []
    
    # Setup parameters based on drug type
    if drug_type == 'marijuana':
        strain_list = list(strain_data.keys())
        if args.strain < 1 or args.strain > len(strain_list):
            print(f"Error: Invalid strain. Must be between 1 and {len(strain_list)}")
            return
            
        strain = strain_list[args.strain - 1]
        effect = strain_data[strain][0]
        units = calculate_units(drug_type, args.grow_tent, args.pgr, drug_pricing['production_units'])
        prod_cost = calculate_cost(
            drug_type, constants, cost_formula, 
            strain=strain, units=units, strain_data=strain_data, 
            ingredient_prices=ingredient_prices
        )
        display, effects = strain, [effect]
    
    elif drug_type == 'meth':
        quality = args.quality
        prod_cost = calculate_cost(
            drug_type, constants, cost_formula, 
            quality=quality, quality_costs=quality_costs
        )
        display = quality_names[quality-1]
    
    else:  # cocaine
        units = calculate_units(drug_type, args.grow_tent, args.pgr, drug_pricing['production_units'])
        prod_cost = calculate_cost(
            drug_type, constants, cost_formula, 
            units=units, ingredient_prices=ingredient_prices
        )
        display = drug_type.capitalize()

    # Initialize the engine and find the best path
    engine = Engine(rules_data, max_effects, effect_priorities)
    result = find_best_path(
        engine, base_price, prod_cost, args.depth, 
        effect_multipliers, ingredient_prices, effect_priorities, effects
    )
    
    if not result:
        print(f"No profitable combination found for {drug_type}")
        return
        
    effects, path, cost = result
    total = get_effects_value(effects, base_price, effect_multipliers)
    profit = total - (prod_cost + cost)
    
    # Display results
    print(f"\nBest Combination for {drug_type} ({display})")
    print(f"Production Cost: ${prod_cost:.2f}")
    print(f"Ingredients ({len(path)}): ${cost:.2f}")
    print(f"Total Cost: ${prod_cost + cost:.2f}")
    print(f"Total Value: ${total}")
    print(f"Profit: ${profit:.2f}")
    print("\nEffects:" + ''.join(f"\n- {e} (x{effect_multipliers[e]:.2f})" for e in effects))
    if path: 
        print("\nRecipe: " + " → ".join(path))
