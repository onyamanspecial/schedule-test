from collections import deque
from math import floor
import argparse
from src.data.loader import load_all_data

MAX_EFFECTS, _, _, EFFECT_PRIORITY, RULES_DATA, EFFECT_MULTIPLIERS, INGREDIENT_PRICES = load_all_data()

DRUG_TYPES = ['marijuana', 'meth', 'cocaine']
MARIJUANA_STRAINS = ['og_kush', 'sour_diesel', 'green_crack', 'granddaddy_purple']
METH_QUALITIES = [1, 2, 3]

STRAIN_DATA = {
    'og_kush': ('Calming', 30),
    'sour_diesel': ('Refreshing', 35),
    'green_crack': ('Energizing', 40),
    'granddaddy_purple': ('Sedating', 45)
}

QUALITY_NAMES = ['Low-Quality Pseudo', 'Pseudo', 'High-Quality Pseudo']
QUALITY_COSTS = [60, 80, 110]

DRUG_CONFIG = {
    'marijuana': {
        'base_price': 35,
        'strains': STRAIN_DATA,
        'units': lambda a,b: 12 if (a and b) else 8 if a else 16 if b else 12,
        'cost': lambda s, u: (STRAIN_DATA[s][1] + 20) / u
    },
    'meth': {
        'base_price': 70,
        'cost': lambda q: (QUALITY_COSTS[q-1] + 80) / 10
    },
    'cocaine': {
        'base_price': 150,
        'units': lambda a,b: 11 if (a and b) else 6 if a else 16 if b else 9,
        'cost': lambda u: 170/u + 0.25
    }
}

def get_effects_value(effects, base_price):
    return floor(base_price * (1 + sum(EFFECT_MULTIPLIERS.get(e, 0) for e in effects)))

class RuleEngine:
    def __init__(self):
        self.ingredient_base = {b:be for b,be,_,_,_ in RULES_DATA if b}
        self.ingredient_base.update({a:ae for _,_,a,_,ae in RULES_DATA if a})
        self.effect_transforms = {(be,a):(re,ae) for _,be,a,re,ae in RULES_DATA if be and a}
    
    def get_transformations(self, effects, ingredient):
        new_effects = list(effects)
        if (ae := self.ingredient_base.get(ingredient)):
            for i, e in enumerate(new_effects):
                if (key := (e, ingredient)) in self.effect_transforms:
                    ne, _ = self.effect_transforms[key]
                    if ne not in new_effects:
                        new_effects[i] = ne
            if ae not in new_effects and len(new_effects) < MAX_EFFECTS:
                new_effects.append(ae)
        return sorted(new_effects, key=lambda x: EFFECT_PRIORITY[x])

def find_best_path(rule_engine, base_price, prod_cost, max_depth, initial=None):
    queue = deque([(0, 0.0, tuple(sorted(initial or [], key=EFFECT_PRIORITY.get)), [])])
    visited = {}
    best_profit, best_state = float('-inf'), None
    
    while queue:
        depth, cost, effects, path = queue.popleft()
        profit = get_effects_value(effects, base_price) - (prod_cost + cost)
        
        if profit > best_profit:
            best_profit, best_state = profit, (effects, path, cost)
            
        if depth < max_depth:
            for ing in rule_engine.ingredient_base:
                new_eff = tuple(rule_engine.get_transformations(list(effects), ing))
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
    m_opts.add_argument('-s', '--strain', type=int, choices=range(1, len(MARIJUANA_STRAINS) + 1),
                        default=1, help=f'Strain: {fmt_choices(MARIJUANA_STRAINS)} (default: 1)')
    
    me_opts = parser.add_argument_group('Meth')
    me_opts.add_argument('-q', '--quality', type=int, choices=range(1, 4),
                         default=3, help='Quality: 1=low | 2=medium | 3=high (default: 3)')
    
    args = parser.parse_args()
    
    # Process drug type and prepare configuration
    drug_type = DRUG_TYPES[args.drug_type - 1]
    cfg = DRUG_CONFIG[drug_type]
    prod_cost, display, effects = 0, '', []
    

    
    # Setup parameters based on drug type
    if drug_type == 'marijuana':
        strain = MARIJUANA_STRAINS[args.strain - 1]
        effect = cfg['strains'][strain][0]
        prod_cost = cfg['cost'](strain, cfg['units'](args.grow_tent, args.pgr))
        display, effects = strain, [effect]
    elif drug_type == 'meth':
        quality = args.quality
        prod_cost = cfg['cost'](quality)
        display = QUALITY_NAMES[quality-1]
    else:  # cocaine
        prod_cost = cfg['cost'](cfg['units'](args.grow_tent, args.pgr))
        display = drug_type.capitalize()

    effects, path, cost = find_best_path(RuleEngine(), cfg['base_price'], prod_cost, args.depth, effects)
    total = get_effects_value(effects, cfg['base_price'])
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