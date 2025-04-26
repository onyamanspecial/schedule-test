from collections import deque
from math import floor
import argparse
from src.data.loader import load_all_data
from src.engine.core import Engine

# Load all required data
MAX_EFFECTS, EFFECTS, EFFECTS_SORTED, EFFECT_PRIORITIES, RULES_DATA, EFFECT_MULTIPLIERS, INGREDIENT_PRICES, \
DRUG_TYPES, STRAIN_DATA, METH_QUALITIES, QUALITY_NAMES, QUALITY_COSTS, DRUG_PRICING = load_all_data()

# Helper function to calculate production units based on configuration
def calculate_units(drug_type, grow_tent, pgr):
    unit_config = DRUG_PRICING['production_units'].get(drug_type)
    if not unit_config or unit_config['formula'] != 'conditional':
        return 1  # Default fallback
    
    for condition, value in unit_config['conditions']:
        if condition == 'grow_tent and pgr' and grow_tent and pgr:
            return value
        elif condition == 'grow_tent' and grow_tent:
            return value
        elif condition == 'pgr' and pgr:
            return value
        elif condition == 'default':
            return value
    return 1  # Default fallback

# Helper function to calculate production cost based on configuration
def calculate_cost(drug_type, strain=None, quality=None, units=None):
    cost_config = DRUG_PRICING['cost_calculations'].get(drug_type)
    if not cost_config:
        return 0
    
    formula = cost_config['formula']
    
    if formula == 'strain_based' and strain:
        strain_cost = STRAIN_DATA[strain][1]
        additional = cost_config.get('additional_cost', 0)
        divisor = units if cost_config.get('divisor') == 'units' else 1
        return (strain_cost + additional) / divisor
    
    elif formula == 'quality_based' and quality is not None:
        quality_cost = QUALITY_COSTS[quality-1]
        additional = cost_config.get('additional_cost', 0)
        divisor = cost_config.get('divisor', 1)
        return (quality_cost + additional) / divisor
    
    elif formula == 'fixed_divisor':
        numerator = cost_config.get('numerator', 0)
        divisor = units if cost_config.get('divisor') == 'units' else cost_config.get('divisor', 1)
        additional = cost_config.get('additional', 0)
        return numerator / divisor + additional
    
    return 0

def get_effects_value(effects, base_price):
    return floor(base_price * (1 + sum(EFFECT_MULTIPLIERS.get(e, 0) for e in effects)))

def find_best_path(engine, base_price, prod_cost, max_depth, initial=None):
    queue = deque([(0, 0.0, tuple(sorted(initial or [], key=lambda x: EFFECT_PRIORITIES[x])), [])])
    visited = {}
    best_profit, best_state = float('-inf'), None
    
    while queue:
        depth, cost, effects, path = queue.popleft()
        profit = get_effects_value(effects, base_price) - (prod_cost + cost)
        
        if profit > best_profit:
            best_profit, best_state = profit, (effects, path, cost)
            
        if depth < max_depth:
            for ing in engine.base_effects:
                new_effects = engine.combine(list(effects), ing)
                new_eff = tuple(new_effects)
                new_cost = cost + INGREDIENT_PRICES.get(ing, 0)
                
                if new_eff not in visited or new_cost < visited[new_eff][0] or profit > visited[new_eff][1]:
                    visited[new_eff] = (new_cost, profit)
                    queue.append((depth+1, new_cost, new_eff, path+[ing]))
                    
    return best_state

def main():
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
    
    parser.add_argument('drug_type', type=int, choices=range(1, len(DRUG_TYPES) + 1),
                        help=f'Drug type: {fmt_choices(DRUG_TYPES)}')
    
    prod = parser.add_argument_group('Production')
    prod.add_argument('-d', '--depth', type=int, default=3, metavar='N',
                      help='Search depth (default: 3)')
    prod.add_argument('-g', '--grow-tent', action='store_true', help='Use grow tent')
    prod.add_argument('-p', '--pgr', action='store_true', help='Use plant growth regulators')
    
    m_opts = parser.add_argument_group('Marijuana')
    m_opts.add_argument('-s', '--strain', type=int, choices=range(1, len(list(STRAIN_DATA.keys())) + 1),
                        default=1, help=f'Strain: {fmt_choices(list(STRAIN_DATA.keys()))} (default: 1)')
    
    me_opts = parser.add_argument_group('Meth')
    me_opts.add_argument('-q', '--quality', type=int, choices=range(1, 4),
                         default=3, help='Quality: 1=low | 2=medium | 3=high (default: 3)')
    
    args = parser.parse_args()
    
    # Process drug type and prepare configuration
    drug_type = DRUG_TYPES[args.drug_type - 1]
    base_price = DRUG_PRICING['base_prices'][drug_type]
    prod_cost, display, effects = 0, '', []
    
    # Setup parameters based on drug type
    if drug_type == 'marijuana':
        strain_list = list(STRAIN_DATA.keys())
        strain = strain_list[args.strain - 1]
        effect = STRAIN_DATA[strain][0]
        units = calculate_units(drug_type, args.grow_tent, args.pgr)
        prod_cost = calculate_cost(drug_type, strain=strain, units=units)
        display, effects = strain, [effect]
    elif drug_type == 'meth':
        quality = args.quality
        prod_cost = calculate_cost(drug_type, quality=quality)
        display = QUALITY_NAMES[quality-1]
    else:  # cocaine
        units = calculate_units(drug_type, args.grow_tent, args.pgr)
        prod_cost = calculate_cost(drug_type, units=units)
        display = drug_type.capitalize()

    # Initialize the engine with the rules data, max effects, and effect priorities
    engine = Engine(RULES_DATA, MAX_EFFECTS, EFFECT_PRIORITIES)
    effects, path, cost = find_best_path(engine, base_price, prod_cost, args.depth, effects)
    total = get_effects_value(effects, base_price)
    profit = total - (prod_cost + cost)
    
    print(f"\nBest Combination for {drug_type} ({display})")
    print(f"Production Cost: ${prod_cost:.2f}")
    print(f"Ingredients ({len(path)}): ${cost:.2f}")
    print(f"Total Cost: ${prod_cost + cost:.2f}")
    print(f"Total Value: ${total}")
    print(f"Profit: ${profit:.2f}")
    print("\nEffects:" + ''.join(f"\n- {e} (x{EFFECT_MULTIPLIERS[e]:.2f})" for e in effects))
    if path: print("\nRecipe: " + " → ".join(path))

if __name__ == "__main__":
    main()