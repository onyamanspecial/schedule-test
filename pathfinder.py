from collections import deque
import argparse

MAX_EFFECTS = 8

PRIORITY_ORDER = [
    'Paranoia', 'Smelly', 'Calming', 'Munchies', 'Refreshing', 'Focused',
    'Euphoric', 'Toxic', 'Disorienting', 'Gingeritis', 'Energizing', 'Sedating',
    'Seizure-Inducing', 'Laxative', 'Balding', 'Calorie-Dense', 'Sneaky',
    'Athletic', 'Slippery', 'Foggy', 'Spicy', 'Jennerising', 'Schizophrenic',
    'Bright-Eyed', 'Thought-Provoking', 'Tropic Thunder', 'Electrifying',
    'Glowing', 'Long faced', 'Anti-gravity', 'Cyclopean', 'Zombifying', 'Shrinking'
]

EFFECT_PRIORITY = {e: i for i, e in enumerate(PRIORITY_ORDER)}
SORTED_EFFECTS = sorted(PRIORITY_ORDER)
EFFECT_IDS = {idx+1: effect for idx, effect in enumerate(SORTED_EFFECTS)}

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

class RuleEngine:
    def __init__(self):
        self.ingredient_base, self.effect_transforms = {}, {}
        for b_ing, b_eff, a_ing, r_eff, a_eff in RULES_DATA:
            if b_ing: self.ingredient_base[b_ing] = b_eff
            if a_ing: self.ingredient_base[a_ing] = a_eff
            if b_eff and a_ing: self.effect_transforms[(b_eff, a_ing)] = (r_eff, a_eff)

    def get_transformations(self, effects, ingredient):
        new_effects = list(effects)
        if (added_eff := self.ingredient_base.get(ingredient)):
            for i, eff in enumerate(new_effects):
                if (key := (eff, ingredient)) in self.effect_transforms:
                    new_eff, _ = self.effect_transforms[key]
                    if new_eff not in new_effects: new_effects[i] = new_eff
            if added_eff not in new_effects and len(new_effects) < MAX_EFFECTS:
                new_effects.append(added_eff)
        return sorted(new_effects, key=lambda x: EFFECT_PRIORITY[x])

def find_path(desired, starting=None):
    engine = RuleEngine()
    starting = sorted(starting or [], key=lambda x: EFFECT_PRIORITY[x])
    if set(desired).issubset(starting): return []
    visited, queue = {tuple(starting)}, deque([(starting, [])])
    while queue:
        effects, path = queue.popleft()
        if set(desired).issubset(effects): return path
        for ing in engine.ingredient_base:
            if (new := engine.get_transformations(effects, ing)):
                if len(new) <= MAX_EFFECTS and (key := tuple(new)) not in visited:
                    visited.add(key)
                    queue.append((new, path + [ing]))
    return None

def parse_effects(input_str):
    effects = []
    for part in input_str.strip().replace(',', ' ').split():
        part = part.strip("'\"")
        if part.isdigit() and int(part) in EFFECT_IDS:
            effects.append(EFFECT_IDS[int(part)])
        elif part in SORTED_EFFECTS:
            effects.append(part)
    return effects

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--desired', required=True, help='Desired effects (comma-separated)')
    parser.add_argument('-s', '--starting', default='', help='Starting effects (comma-separated)')
    parser.add_argument('-l', '--list', action='store_true', help='List available effects')
    args = parser.parse_args()

    if args.list:
        for idx, effect in enumerate(SORTED_EFFECTS, 1):
            print(f"{idx}: {effect}")
        return

    desired = parse_effects(args.desired)
    starting = parse_effects(args.starting)
    if not desired:
        return print("No valid desired effects")

    path = find_path(desired, starting)
    if path:
        print(' → '.join(path))
    else:
        print("No solution")

if __name__ == "__main__":
    main()