from collections import deque
from math import floor
import argparse, json

# Configuration
MAX_EFFECTS = 8
GASOLINE_PER_COCAINE_UNIT = 1/20

# Processing priority (highest to lowest)
PRIORITY_ORDER = [
    'Paranoia', 'Smelly', 'Calming', 'Munchies', 'Refreshing', 'Focused',
    'Euphoric', 'Toxic', 'Disorienting', 'Gingeritis', 'Energizing', 'Sedating',
    'Seizure-Inducing', 'Laxative', 'Balding', 'Calorie-Dense', 'Sneaky',
    'Athletic', 'Slippery', 'Foggy', 'Spicy', 'Jennerising', 'Schizophrenic',
    'Bright-Eyed', 'Thought-Provoking', 'Tropic Thunder', 'Electrifying',
    'Glowing', 'Long faced', 'Anti-gravity', 'Cyclopean', 'Zombifying', 'Shrinking'
]

# Precompute priority index for O(1) lookups
EFFECT_PRIORITY = {e: i for i, e in enumerate(PRIORITY_ORDER)}

# Complete rule set
RULES_DATA = [
    ("Addy", "Thought-Provoking", "Flu Medicine", "Gingeritis", "Sedating"),
    ("Addy", "Thought-Provoking", "Horse Semen", "Electrifying", "Long faced"),
    ("Addy", "Thought-Provoking", "Mega Bean", "Energizing", "Foggy"),
    ("Banana", "Gingeritis", "Cuke", "Thought-Provoking", "Energizing"),
    ("Banana", "Gingeritis", "Gasoline", "Smelly", "Toxic"),
    ("Banana", "Gingeritis", "Horse Semen", "Refreshing", "Long faced"),
    ("Battery", "Bright-Eyed", "", "", ""),
    ("Chili", "Spicy", "Energy Drink", "Euphoric", "Athletic"),
    ("Chili", "Spicy", "Paracetamol", "Bright-Eyed", "Sneaky"),
    ("Cuke", "Energizing", "Banana", "Thought-Provoking", "Gingeritis"),
    ("Cuke", "Energizing", "Gasoline", "Euphoric", "Toxic"),
    ("Cuke", "Energizing", "Mega Bean", "Cyclopean", "Foggy"),
    ("Cuke", "Energizing", "Motor Oil", "Munchies", "Slippery"),
    ("Cuke", "Energizing", "Paracetamol", "Paranoia", "Sneaky"),
    ("Donut", "Calorie-Dense", "Iodine", "Gingeritis", "Jennerising"),
    ("Donut", "Calorie-Dense", "Mouth Wash", "Sneaky", "Balding"),
    ("Energy Drink", "Athletic", "Chili", "Euphoric", "Spicy"),
    ("Energy Drink", "Athletic", "Flu Medicine", "Munchies", "Sedating"),
    ("Energy Drink", "Athletic", "Mega Bean", "Laxative", "Foggy"),
    ("Energy Drink", "Athletic", "Viagra", "Sneaky", "Tropic Thunder"),
    ("Flu Medicine", "Sedating", "Addy", "Gingeritis", "Thought-Provoking"),
    ("Flu Medicine", "Sedating", "Energy Drink", "Munchies", "Athletic"),
    ("Gasoline", "Toxic", "Banana", "Smelly", "Gingeritis"),
    ("Gasoline", "Toxic", "Cuke", "Euphoric", "Energizing"),
    ("Gasoline", "Toxic", "Iodine", "Sneaky", "Jennerising"),
    ("Gasoline", "Toxic", "Paracetamol", "Tropic Thunder", "Sneaky"),
    ("Horse Semen", "Long faced", "Addy", "Electrifying", "Thought-Provoking"),
    ("Horse Semen", "Long faced", "Banana", "Refreshing", "Gingeritis"),
    ("Iodine", "Jennerising", "Donut", "Gingeritis", "Calorie-Dense"),
    ("Iodine", "Jennerising", "Gasoline", "Sneaky", "Toxic"),
    ("Iodine", "Jennerising", "Mega Bean", "Paranoia", "Foggy"),
    ("Mega Bean", "Foggy", "Addy", "Energizing", "Thought-Provoking"),
    ("Mega Bean", "Foggy", "Cuke", "Cyclopean", "Energizing"),
    ("Mega Bean", "Foggy", "Energy Drink", "Laxative", "Athletic"),
    ("Mega Bean", "Foggy", "Iodine", "Paranoia", "Jennerising"),
    ("Mega Bean", "Foggy", "Motor Oil", "Toxic", "Slippery"),
    ("Mega Bean", "Foggy", "Paracetamol", "Calming", "Sneaky"),
    ("Motor Oil", "Slippery", "Cuke", "Munchies", "Energizing"),
    ("Motor Oil", "Slippery", "Mega Bean", "Toxic", "Foggy"),
    ("Mouth Wash", "Balding", "Donut", "Sneaky", "Calorie-Dense"),
    ("Paracetamol", "Sneaky", "Chili", "Bright-Eyed", "Spicy"),
    ("Paracetamol", "Sneaky", "Cuke", "Paranoia", "Energizing"),
    ("Paracetamol", "Sneaky", "Gasoline", "Tropic Thunder", "Toxic"),
    ("Paracetamol", "Sneaky", "Mega Bean", "Calming", "Foggy"),
    ("Viagra", "Tropic Thunder", "Energy Drink", "Sneaky", "Athletic"),
    ("", "Calming", "Banana", "Sneaky", "Gingeritis"),
    ("", "Calming", "Flu Medicine", "Bright-Eyed", "Sedating"),
    ("", "Calming", "Iodine", "Balding", "Jennerising"),
    ("", "Calming", "Mega Bean", "Glowing", "Foggy"),
    ("", "Calming", "Mouth Wash", "Anti-gravity", "Balding"),
    ("", "Calming", "Paracetamol", "Slippery", "Sneaky"),
    ("", "Refreshing", "Iodine", "Thought-Provoking", "Jennerising"),
    ("", "Energizing", "Banana", "Thought-Provoking", "Gingeritis"),
    ("", "Energizing", "Gasoline", "Euphoric", "Toxic"),
    ("", "Energizing", "Mega Bean", "Cyclopean", "Foggy"),
    ("", "Energizing", "Motor Oil", "Munchies", "Slippery"),
    ("", "Energizing", "Paracetamol", "Paranoia", "Sneaky"),
    ("", "Sedating", "Energy Drink", "Munchies", "Athletic"),
    ("", "Anti-gravity", "Chili", "Tropic Thunder", "Spicy"),
    ("", "Anti-gravity", "Donut", "Slippery", "Calorie-Dense"),
    ("", "Anti-gravity", "Horse Semen", "Calming", "Long faced"),
    ("", "Cyclopean", "Banana", "Energizing", "Gingeritis"),
    ("", "Cyclopean", "Battery", "Glowing", "Bright-Eyed"),
    ("", "Cyclopean", "Flu Medicine", "Foggy", "Sedating"),
    ("", "Disorienting", "Banana", "Focused", "Gingeritis"),
    ("", "Disorienting", "Energy Drink", "Electrifying", "Athletic"),
    ("", "Disorienting", "Gasoline", "Glowing", "Toxic"),
    ("", "Electrifying", "Battery", "Euphoric", "Bright-Eyed"),
    ("", "Electrifying", "Flu Medicine", "Refreshing", "Sedating"),
    ("", "Electrifying", "Gasoline", "Disorienting", "Toxic"),
    ("", "Electrifying", "Paracetamol", "Athletic", "Sneaky"),
    ("", "Euphoric", "Battery", "Zombifying", "Bright-Eyed"),
    ("", "Euphoric", "Energy Drink", "Energizing", "Athletic"),
    ("", "Euphoric", "Gasoline", "Spicy", "Toxic"),
    ("", "Euphoric", "Iodine", "Seizure-Inducing", "Jennerising"),
    ("", "Euphoric", "Motor Oil", "Sedating", "Slippery"),
    ("", "Euphoric", "Viagra", "Bright-Eyed", "Tropic Thunder"),
    ("", "Focused", "Banana", "Seizure-Inducing", "Gingeritis"),
    ("", "Focused", "Donut", "Euphoric", "Calorie-Dense"),
    ("", "Focused", "Energy Drink", "Shrinking", "Athletic"),
    ("", "Focused", "Flu Medicine", "Bright-Eyed", "Sedating"),
    ("", "Focused", "Mega Bean", "Disorienting", "Foggy"),
    ("", "Focused", "Mouth Wash", "Jennerising", "Balding"),
    ("", "Glowing", "Addy", "Refreshing", "Thought-Provoking"),
    ("", "Glowing", "Energy Drink", "Disorienting", "Athletic"),
    ("", "Glowing", "Paracetamol", "Toxic", "Sneaky"),
    ("", "Laxative", "Battery", "Calorie-Dense", "Bright-Eyed"),
    ("", "Laxative", "Chili", "Long faced", "Spicy"),
    ("", "Laxative", "Flu Medicine", "Euphoric", "Sedating"),
    ("", "Laxative", "Gasoline", "Foggy", "Toxic"),
    ("", "Laxative", "Viagra", "Calming", "Tropic Thunder"),
    ("", "Munchies", "Battery", "Tropic Thunder", "Bright-Eyed"),
    ("", "Munchies", "Chili", "Toxic", "Spicy"),
    ("", "Munchies", "Cuke", "Athletic", "Energizing"),
    ("", "Munchies", "Donut", "Calming", "Calorie-Dense"),
    ("", "Munchies", "Gasoline", "Sedating", "Toxic"),
    ("", "Munchies", "Motor Oil", "Schizophrenic", "Slippery"),
    ("", "Munchies", "Paracetamol", "Anti-gravity", "Sneaky"),
    ("", "Paranoia", "Banana", "Jennerising", "Gingeritis"),
    ("", "Paranoia", "Gasoline", "Calming", "Toxic"),
    ("", "Paranoia", "Motor Oil", "Anti-gravity", "Slippery"),
    ("", "Paranoia", "Paracetamol", "Balding", "Sneaky"),
    ("", "Schizophrenic", "Energy Drink", "Balding", "Athletic"),
    ("", "Seizure-Inducing", "Horse Semen", "Energizing", "Long faced"),
    ("", "Seizure-Inducing", "Mega Bean", "Focused", "Foggy"),
    ("", "Shrinking", "Battery", "Munchies", "Bright-Eyed"),
    ("", "Shrinking", "Chili", "Refreshing", "Spicy"),
    ("", "Shrinking", "Donut", "Energizing", "Calorie-Dense"),
    ("", "Shrinking", "Flu Medicine", "Paranoia", "Sedating"),
    ("", "Shrinking", "Gasoline", "Focused", "Toxic"),
    ("", "Shrinking", "Mega Bean", "Electrifying", "Foggy"),
    ("", "Shrinking", "Viagra", "Gingeritis", "Tropic Thunder"),
    ("", "Smelly", "Banana", "Anti-gravity", "Gingeritis"),
    ("Zombifying", "", "", "", "")
]

# Ingredient prices
INGREDIENT_PRICES = {
    'Addy': 9, 'Banana': 2, 'Battery': 8, 'Chili': 7, 'Cuke': 2, 'Donut': 3,
    'Energy Drink': 6, 'Flu Medicine': 5, 'Gasoline': 5, 'Horse Semen': 9,
    'Iodine': 9, 'Mega Bean': 7, 'Motor Oil': 6, 'Mouth Wash': 4,
    'Paracetamol': 3, 'Viagra': 4
}

# Effect multipliers
EFFECT_MULTIPLIERS = {
    'Anti-gravity': 0.54,
    'Athletic': 0.32,
    'Balding': 0.30,
    'Bright-Eyed': 0.40,
    'Calming': 0.10,
    'Calorie-Dense': 0.28,
    'Cyclopean': 0.56,
    'Disorienting': 0.00,
    'Electrifying': 0.50,
    'Energizing': 0.22,
    'Euphoric': 0.18,
    'Focused': 0.16,
    'Foggy': 0.36,
    'Gingeritis': 0.20,
    'Glowing': 0.48,
    'Jennerising': 0.42,
    'Laxative': 0.00,
    'Long faced': 0.52,
    'Munchies': 0.12,
    'Paranoia': 0.00,
    'Refreshing': 0.14,
    'Schizophrenic': 0.00,
    'Sedating': 0.26,
    'Seizure-Inducing': 0.00,
    'Shrinking': 0.60,
    'Slippery': 0.34,
    'Smelly': 0.00,
    'Sneaky': 0.24,
    'Spicy': 0.38,
    'Thought-Provoking': 0.44,
    'Toxic': 0.00,
    'Tropic Thunder': 0.46,
    'Zombifying': 0.58
}

# Production cost components
PLANT_SOIL_COST = 60
PLANT_SOIL_USES = 3
METH_ACID_COST = 40
METH_PHOSPHORUS_COST = 40
METH_BATCH_SIZE = 10

DRUG_CONFIG = {
    'marijuana': {
        'base_price': 35,
        'strains': {
            'og_kush': ('Calming', 30),
            'sour_diesel': ('Refreshing', 35),
            'green_crack': ('Energizing', 40),
            'granddaddy_purple': ('Sedating', 45)
        },
        'units': lambda gt, pgr: 12 if (gt and pgr) else 8 if gt else 16 if pgr else 12,
        'cost': lambda strain, units: (DRUG_CONFIG['marijuana']['strains'][strain][1] + 20) / units
    },
    'meth': {
        'base_price': 70,
        'qualities': {
            'low': ('Low-Quality Pseudo', 60),
            'medium': ('Pseudo', 80),
            'high': ('High-Quality Pseudo', 110)
        },
        'cost': lambda quality: (DRUG_CONFIG['meth']['qualities'][quality][1] + 80) / 10
    },
    'cocaine': {
        'base_price': 150,
        'units': lambda gt, pgr: 11 if (gt and pgr) else 6 if gt else 16 if pgr else 9,
        'cost': lambda units: 170/units + 0.25
    }
}

def get_effects_value(effects, base_price):
    return floor(base_price * (1 + sum(EFFECT_MULTIPLIERS.get(e, 0) for e in effects)))

class RuleEngine:
    def __init__(self):
        self.ingredient_base, self.effect_transforms = {}, {}
        for base_ing, base_eff, added_ing, res_eff, added_eff in RULES_DATA:
            if base_ing: self.ingredient_base[base_ing] = base_eff
            if added_ing: self.ingredient_base[added_ing] = added_eff
            if base_eff and added_ing:
                self.effect_transforms[(base_eff, added_ing)] = (res_eff, added_eff)
    
    def get_transformations(self, effects, ingredient):
        new_effects = list(effects)
        if (added_eff := self.ingredient_base.get(ingredient)):
            for i, eff in enumerate(new_effects):
                if (key := (eff, ingredient)) in self.effect_transforms:
                    new_eff, _ = self.effect_transforms[key]
                    if new_eff not in new_effects:
                        new_effects[i] = new_eff
            if added_eff not in new_effects and len(new_effects) < MAX_EFFECTS:
                new_effects.append(added_eff)
        return sorted(new_effects, key=lambda x: EFFECT_PRIORITY[x])

def find_best_path(rule_engine, base_price, production_cost, max_depth, initial_effects=None):
    visited, queue = {}, deque([(0, 0.0, tuple(sorted(initial_effects or [], key=EFFECT_PRIORITY.get)), [])])
    best_state = None
    best_profit = float('-inf')
    
    while queue:
        depth, total_cost, effects, path = queue.popleft()
        if (profit := get_effects_value(effects, base_price) - (production_cost + total_cost)) > best_profit:
            best_profit, best_state = profit, (effects, path, total_cost)
        
        if depth < max_depth:
            for ingredient in rule_engine.ingredient_base:
                new_effects = tuple(sorted(rule_engine.get_transformations(list(effects), ingredient), 
                                        key=EFFECT_PRIORITY.get))
                new_cost = total_cost + INGREDIENT_PRICES.get(ingredient, 0)
                
                if new_effects not in visited or new_cost < visited[new_effects][0] or profit > visited[new_effects][1]:
                    visited[new_effects] = (new_cost, profit)
                    queue.append((depth + 1, new_cost, new_effects, path + [ingredient]))
    
    return best_state

def main():
    parser = argparse.ArgumentParser(description='Drug Combination Optimizer')
    parser.add_argument('drug_type', choices=list(DRUG_CONFIG))
    parser.add_argument('--depth', type=int, default=3)
    parser.add_argument('--grow-tent', action='store_true')
    parser.add_argument('--pgr', action='store_true')
    parser.add_argument('--strain', choices=list(DRUG_CONFIG['marijuana']['strains']))
    parser.add_argument('--quality', choices=list(DRUG_CONFIG['meth']['qualities']))
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    config = DRUG_CONFIG[args.drug_type]
    
    if args.drug_type == 'marijuana':
        effect = config['strains'][args.strain][0]
        production_cost = config['cost'](args.strain, config['units'](args.grow_tent, args.pgr))
        starting_effects = [effect]
        display_subtype = args.strain
    elif args.drug_type == 'meth':
        production_cost = config['cost'](args.quality)
        display_subtype = config['qualities'][args.quality][0]
        starting_effects = []
    else:
        production_cost = config['cost'](config['units'](args.grow_tent, args.pgr))
        display_subtype = 'Cocaine'
        starting_effects = []

    best_state = find_best_path(RuleEngine(), config['base_price'], production_cost, args.depth, starting_effects)
    effects, path, ingredient_cost = best_state
    total_value = get_effects_value(effects, config['base_price'])
    total_cost = production_cost + ingredient_cost
    profit = total_value - total_cost
    
    if args.json:
        print(json.dumps({
            'drug_type': args.drug_type,
            'subtype': display_subtype,
            'production_cost': round(production_cost, 2),
            'ingredients': {'count': len(path), 'cost': round(ingredient_cost, 2), 'list': path},
            'total_cost': round(total_cost, 2),
            'total_value': total_value,
            'profit': round(profit, 2),
            'effects': [{'name': e, 'multiplier': round(EFFECT_MULTIPLIERS[e], 2)} for e in effects]
        }, indent=2))
    else:
        print(f"\nBest Combination for {args.drug_type} ({display_subtype})")
        print(f"Production Cost: ${production_cost:.2f}")
        print(f"Ingredients ({len(path)}): ${ingredient_cost:.2f}")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Total Value: ${total_value:.2f}")
        print(f"Total Profit: ${profit:.2f}")
        print("\nEffects:", *[f"\n- {e} (x{EFFECT_MULTIPLIERS[e]:.2f})" for e in effects])
        if path: print("\nRecipe:", " → ".join(path))

if __name__ == "__main__":
    main()