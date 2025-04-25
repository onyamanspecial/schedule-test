from collections import deque
import time

MAX_EFFECTS = 8

PRIORITY_ORDER = [
    'Paranoia', 'Smelly', 'Calming', 'Munchies', 'Refreshing', 'Focused',
    'Euphoric', 'Toxic', 'Disorienting', 'Gingeritis', 'Energizing', 'Sedating',
    'Seizure-Inducing', 'Laxative', 'Balding', 'Calorie-Dense', 'Sneaky',
    'Athletic', 'Slippery', 'Foggy', 'Spicy', 'Jennerising', 'Schizophrenic',
    'Bright-Eyed', 'Thought-Provoking', 'Tropic Thunder', 'Electrifying',
    'Glowing', 'Long faced', 'Anti-gravity', 'Cyclopean', 'Zombifying', 'Shrinking'
]

EFFECT_PRIORITY = {effect: idx for idx, effect in enumerate(PRIORITY_ORDER)}
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
        self.ingredient_base = {}
        self.effect_transforms = {}
        for rule in RULES_DATA:
            base_ing, base_eff, added_ing, res_eff, added_eff = rule
            if base_ing:
                self.ingredient_base[base_ing] = base_eff
            if added_ing:
                self.ingredient_base[added_ing] = added_eff
            if base_eff and added_ing:
                self.effect_transforms[(base_eff, added_ing)] = (res_eff, added_eff)

    def get_transformations(self, current_effects, ingredient):
        new_effects = list(current_effects)
        added_eff = self.ingredient_base.get(ingredient)
        for i, eff in enumerate(new_effects):
            key = (eff, ingredient)
            if key in self.effect_transforms:
                new_eff, _ = self.effect_transforms[key]
                if new_eff not in new_effects:
                    new_effects[i] = new_eff
        if added_eff and added_eff not in new_effects and len(new_effects) < MAX_EFFECTS:
            new_effects.append(added_eff)
        return sorted(new_effects, key=lambda x: EFFECT_PRIORITY[x])

def display_effects():
    print("\n" + "="*80)
    print("Available Effects (ID: Name)".center(80))
    print("="*80)
    cols = 3
    total = len(SORTED_EFFECTS)
    rows = (total + cols - 1) // cols
    for row in range(rows):
        line = []
        for col in range(cols):
            idx = row + col * rows
            if idx < total:
                effect_id = idx + 1
                name = SORTED_EFFECTS[idx]
                line.append(f"[{effect_id:2d}] {name:20}")
            else:
                line.append(" " * 25)
        print("  ".join(line))
    print("="*80 + "\n")

def parse_effects(input_str):
    parts = input_str.strip().replace(',', ' ').replace('_', ' ').split()
    effects = []
    for part in parts:
        part = part.strip("'\"")
        if part.isdigit():
            eid = int(part)
            if eid in EFFECT_IDS:
                effects.append(EFFECT_IDS[eid])
        else:
            if part in SORTED_EFFECTS:
                effects.append(part)
    return effects

def show_progress(processed, queue_size, start_time):
    elapsed = time.time() - start_time
    total = processed + queue_size
    eta = (elapsed / processed) * queue_size if processed > 0 else 0
    status = f"⏳ Processed: {processed:6d} | Queue: {queue_size:6d} | Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s"
    print(f"\r{status}", end='', flush=True)

class PathFinder:
    def __init__(self, rule_engine):
        self.rule_engine = rule_engine

    def find_shortest_path(self, desired, starting=None):
        starting = starting or []
        desired_set = set(desired)
        starting_sorted = sorted(starting, key=lambda x: EFFECT_PRIORITY[x])
        if desired_set.issubset(starting_sorted):
            return []
        visited = set()
        queue = deque([(starting_sorted, [])])
        visited.add(tuple(starting_sorted))
        start_time = time.time()
        processed = 0
        while queue:
            current_effects, path = queue.popleft()
            if desired_set.issubset(current_effects):
                return path
            for ingredient in self.rule_engine.ingredient_base:
                new_effects = self.rule_engine.get_transformations(current_effects, ingredient)
                if len(new_effects) > MAX_EFFECTS:
                    continue
                state_key = tuple(new_effects)
                if state_key not in visited:
                    visited.add(state_key)
                    queue.append((new_effects, path + [ingredient]))
            processed += 1
            if processed % 100 == 0:
                show_progress(processed, len(queue), start_time)
        return None

def simulate_mixing(starting, path, rule_engine):
    current = list(starting)
    steps = []
    for step, ingredient in enumerate(path, 1):
        previous = list(current)
        current = rule_engine.get_transformations(current, ingredient)
        steps.append({
            'step': step,
            'ingredient': ingredient,
            'previous': previous,
            'current': current
        })
    return steps

def main():
    rule_engine = RuleEngine()
    path_finder = PathFinder(rule_engine)
    while True:
        display_effects()
        desired_input = input("\n🎯 Desired effects: ")
        starting_input = input("🧪 Starting effects: ")
        desired = parse_effects(desired_input)
        starting = parse_effects(starting_input)
        if not desired:
            continue
        print("\n🚀 Starting search...")
        path = path_finder.find_shortest_path(desired, starting)
        if path:
            print("\n✅ Solution Found!")
            steps = simulate_mixing(starting or [], path, rule_engine)
            for step in steps:
                print(f"\n{'─'*60}")
                print(f" Step {step['step']:2d}: Add {step['ingredient']}")
                print(f" Previous: {', '.join(step['previous']) or 'None'}")
                print(f" Result:   {', '.join(step['current'])} ({len(step['current'])}/{MAX_EFFECTS})")
            print("\n✅ Final Recipe:")
            print(" → ".join(path))
        else:
            print("\n❌ No solution found under current constraints")
        response = input("\n🔄 Try another combination? (Y/N or press Enter to continue): ").strip().lower()
        if response == 'n':
            break

if __name__ == "__main__":
    main()