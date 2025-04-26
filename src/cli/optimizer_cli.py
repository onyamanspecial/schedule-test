import argparse
from typing import List, Dict, Tuple, Any
from src.engine.core import Engine
from src.engine.optimizer import find_best_path, calculate_units, calculate_cost, get_effects_value

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser for the optimizer.
    
    Returns:
        Configured ArgumentParser instance
    """
    def fmt_choices(items):
        return " | ".join(f"{i+1}={item}" for i, item in enumerate(items))
    
    class CapitalizationHelpFormatter(argparse.HelpFormatter):
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
    
    parser = argparse.ArgumentParser(
        description='Drug Optimizer',
        formatter_class=CapitalizationHelpFormatter)
    
    parser.add_argument('drug_type', type=int, choices=range(1, 4),
                        help=f'Drug type: 1=marijuana | 2=meth | 3=cocaine')
    
    prod = parser.add_argument_group('Production')
    prod.add_argument('-d', '--depth', type=int, default=3, metavar='N',
                      help='Search depth (default: 3)')
    prod.add_argument('-g', '--grow-tent', action='store_true', help='Use grow tent')
    prod.add_argument('-p', '--pgr', action='store_true', help='Use plant growth regulators')
    
    m_opts = parser.add_argument_group('Marijuana')
    m_opts.add_argument('-s', '--strain', type=int, choices=range(1, 5),
                        default=1, help='Strain: 1=og_kush | 2=sour_diesel | 3=green_crack | 4=granddaddy_purple (default: 1)')
    
    me_opts = parser.add_argument_group('Meth')
    me_opts.add_argument('-q', '--quality', type=int, choices=range(1, 4),
                         default=3, help='Quality: 1=low | 2=medium | 3=high (default: 3)')
    
    return parser

def run_optimizer(drug_types: List[str], strain_data: Dict[str, Tuple[str, int]], 
                 quality_names: List[str], quality_costs: List[int],
                 drug_pricing: Dict[str, Any], engine: Engine, 
                 effect_priorities: Dict[str, int], ingredient_prices: Dict[str, int],
                 effect_multipliers: Dict[str, float], args: argparse.Namespace) -> None:
    """Run the optimizer with the given arguments and print the results.
    
    Args:
        drug_types: List of available drug types
        strain_data: Dictionary mapping marijuana strains to their effects and costs
        quality_names: List of names for different meth qualities
        quality_costs: List of costs for different meth qualities
        drug_pricing: Drug pricing configuration dictionary
        engine: Engine instance containing combination rules
        effect_priorities: Dictionary mapping effects to their sort priorities
        ingredient_prices: Dictionary mapping ingredients to their prices
        effect_multipliers: Dictionary mapping effects to their value multipliers
        args: Command-line arguments
    """
    # Process drug type and prepare configuration
    drug_type = drug_types[args.drug_type - 1]
    base_price = drug_pricing['base_prices'][drug_type]
    prod_cost, display, effects = 0, '', []
    
    # Setup parameters based on drug type
    if drug_type == 'marijuana':
        strain_list = list(strain_data.keys())
        strain = strain_list[args.strain - 1]
        effect = strain_data[strain][0]
        units = calculate_units(drug_type, args.grow_tent, args.pgr, drug_pricing['production_units'])
        prod_cost = calculate_cost(
            drug_type, drug_pricing['constants'], drug_pricing['cost_calculations'],
            strain_data, quality_costs, ingredient_prices, strain=strain, units=units
        )
        display, effects = strain, [effect]
    elif drug_type == 'meth':
        quality = args.quality
        prod_cost = calculate_cost(
            drug_type, drug_pricing['constants'], drug_pricing['cost_calculations'],
            strain_data, quality_costs, ingredient_prices, quality=quality
        )
        display = quality_names[quality-1]
    else:  # cocaine
        units = calculate_units(drug_type, args.grow_tent, args.pgr, drug_pricing['production_units'])
        prod_cost = calculate_cost(
            drug_type, drug_pricing['constants'], drug_pricing['cost_calculations'],
            strain_data, quality_costs, ingredient_prices, units=units
        )
        display = drug_type.capitalize()

    # Find the best path
    effects, path, cost = find_best_path(
        engine, base_price, prod_cost, args.depth, 
        effect_priorities, ingredient_prices, effect_multipliers, effects
    )
    total = get_effects_value(effects, base_price, effect_multipliers)
    profit = total - (prod_cost + cost)
    
    # Print the results
    print(f"\nBest Combination for {drug_type} ({display})")
    print(f"Production Cost: ${prod_cost:.2f}")
    print(f"Ingredients ({len(path)}): ${cost:.2f}")
    print(f"Total Cost: ${prod_cost + cost:.2f}")
    print(f"Total Value: ${total}")
    print(f"Profit: ${profit:.2f}")
    print("\nEffects:" + ''.join(f"\n- {e} (x{effect_multipliers[e]:.2f})" for e in effects))
    if path: print("\nRecipe: " + " → ".join(path))
