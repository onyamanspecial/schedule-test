from collections import deque
import argparse

MAX_EFFECTS = 8
EFFECTS = ['Paranoia','Smelly','Calming','Munchies','Refreshing','Focused','Euphoric','Toxic','Disorienting','Gingeritis','Energizing','Sedating','Seizure-Inducing','Laxative','Balding','Calorie-Dense','Sneaky','Athletic','Slippery','Foggy','Spicy','Jennerising','Schizophrenic','Bright-Eyed','Thought-Provoking','Tropic Thunder','Electrifying','Glowing','Long faced','Anti-gravity','Cyclopean','Zombifying','Shrinking']
EFFECT_PRIORITIES = {effect: priority for priority, effect in enumerate(EFFECTS)}
EFFECTS_SORTED = sorted(EFFECTS)

RECIPES = [("Addy","Thought-Provoking","Flu Medicine","Gingeritis","Sedating"),("Addy","Thought-Provoking","Horse Semen","Electrifying","Long faced"),("Addy","Thought-Provoking","Mega Bean","Energizing","Foggy"),("Banana","Gingeritis","Cuke","Thought-Provoking","Energizing"),("Banana","Gingeritis","Gasoline","Smelly","Toxic"),("Banana","Gingeritis","Horse Semen","Refreshing","Long faced"),("Battery","Bright-Eyed","","",""),("Chili","Spicy","Energy Drink","Euphoric","Athletic"),("Chili","Spicy","Paracetamol","Bright-Eyed","Sneaky"),("Cuke","Energizing","Banana","Thought-Provoking","Gingeritis"),("Cuke","Energizing","Gasoline","Euphoric","Toxic"),("Cuke","Energizing","Mega Bean","Cyclopean","Foggy"),("Cuke","Energizing","Motor Oil","Munchies","Slippery"),("Cuke","Energizing","Paracetamol","Paranoia","Sneaky"),("Donut","Calorie-Dense","Iodine","Gingeritis","Jennerising"),("Donut","Calorie-Dense","Mouth Wash","Sneaky","Balding"),("Energy Drink","Athletic","Chili","Euphoric","Spicy"),("Energy Drink","Athletic","Flu Medicine","Munchies","Sedating"),("Energy Drink","Athletic","Mega Bean","Laxative","Foggy"),("Energy Drink","Athletic","Viagra","Sneaky","Tropic Thunder"),("Flu Medicine","Sedating","Addy","Gingeritis","Thought-Provoking"),("Flu Medicine","Sedating","Energy Drink","Munchies","Athletic"),("Gasoline","Toxic","Banana","Smelly","Gingeritis"),("Gasoline","Toxic","Cuke","Euphoric","Energizing"),("Gasoline","Toxic","Iodine","Sneaky","Jennerising"),("Gasoline","Toxic","Paracetamol","Tropic Thunder","Sneaky"),("Horse Semen","Long faced","Addy","Electrifying","Thought-Provoking"),("Horse Semen","Long faced","Banana","Refreshing","Gingeritis"),("Iodine","Jennerising","Donut","Gingeritis","Calorie-Dense"),("Iodine","Jennerising","Gasoline","Sneaky","Toxic"),("Iodine","Jennerising","Mega Bean","Paranoia","Foggy"),("Mega Bean","Foggy","Addy","Energizing","Thought-Provoking"),("Mega Bean","Foggy","Cuke","Cyclopean","Energizing"),("Mega Bean","Foggy","Energy Drink","Laxative","Athletic"),("Mega Bean","Foggy","Iodine","Paranoia","Jennerising"),("Mega Bean","Foggy","Motor Oil","Toxic","Slippery"),("Mega Bean","Foggy","Paracetamol","Calming","Sneaky"),("Motor Oil","Slippery","Cuke","Munchies","Energizing"),("Motor Oil","Slippery","Mega Bean","Toxic","Foggy"),("Mouth Wash","Balding","Donut","Sneaky","Calorie-Dense"),("Paracetamol","Sneaky","Chili","Bright-Eyed","Spicy"),("Paracetamol","Sneaky","Cuke","Paranoia","Energizing"),("Paracetamol","Sneaky","Gasoline","Tropic Thunder","Toxic"),("Paracetamol","Sneaky","Mega Bean","Calming","Foggy"),("Viagra","Tropic Thunder","Energy Drink","Sneaky","Athletic"),("","Calming","Banana","Sneaky","Gingeritis"),("","Calming","Flu Medicine","Bright-Eyed","Sedating"),("","Calming","Iodine","Balding","Jennerising"),("","Calming","Mega Bean","Glowing","Foggy"),("","Calming","Mouth Wash","Anti-gravity","Balding"),("","Calming","Paracetamol","Slippery","Sneaky"),("","Refreshing","Iodine","Thought-Provoking","Jennerising"),("","Energizing","Banana","Thought-Provoking","Gingeritis"),("","Energizing","Gasoline","Euphoric","Toxic"),("","Energizing","Mega Bean","Cyclopean","Foggy"),("","Energizing","Motor Oil","Munchies","Slippery"),("","Energizing","Paracetamol","Paranoia","Sneaky"),("","Sedating","Energy Drink","Munchies","Athletic"),("","Anti-gravity","Chili","Tropic Thunder","Spicy"),("","Anti-gravity","Donut","Slippery","Calorie-Dense"),("","Anti-gravity","Horse Semen","Calming","Long faced"),("","Cyclopean","Banana","Energizing","Gingeritis"),("","Cyclopean","Battery","Glowing","Bright-Eyed"),("","Cyclopean","Flu Medicine","Foggy","Sedating"),("","Disorienting","Banana","Focused","Gingeritis"),("","Disorienting","Energy Drink","Electrifying","Athletic"),("","Disorienting","Gasoline","Glowing","Toxic"),("","Electrifying","Battery","Euphoric","Bright-Eyed"),("","Electrifying","Flu Medicine","Refreshing","Sedating"),("","Electrifying","Gasoline","Disorienting","Toxic"),("","Electrifying","Paracetamol","Athletic","Sneaky"),("","Euphoric","Battery","Zombifying","Bright-Eyed"),("","Euphoric","Energy Drink","Energizing","Athletic"),("","Euphoric","Gasoline","Spicy","Toxic"),("","Euphoric","Iodine","Seizure-Inducing","Jennerising"),("","Euphoric","Motor Oil","Sedating","Slippery"),("","Euphoric","Viagra","Bright-Eyed","Tropic Thunder"),("","Focused","Banana","Seizure-Inducing","Gingeritis"),("","Focused","Donut","Euphoric","Calorie-Dense"),("","Focused","Energy Drink","Shrinking","Athletic"),("","Focused","Flu Medicine","Bright-Eyed","Sedating"),("","Focused","Mega Bean","Disorienting","Foggy"),("","Focused","Mouth Wash","Jennerising","Balding"),("","Glowing","Addy","Refreshing","Thought-Provoking"),("","Glowing","Energy Drink","Disorienting","Athletic"),("","Glowing","Paracetamol","Toxic","Sneaky"),("","Laxative","Battery","Calorie-Dense","Bright-Eyed"),("","Laxative","Chili","Long faced","Spicy"),("","Laxative","Flu Medicine","Euphoric","Sedating"),("","Laxative","Gasoline","Foggy","Toxic"),("","Laxative","Viagra","Calming","Tropic Thunder"),("","Munchies","Battery","Tropic Thunder","Bright-Eyed"),("","Munchies","Chili","Toxic","Spicy"),("","Munchies","Cuke","Athletic","Energizing"),("","Munchies","Donut","Calming","Calorie-Dense"),("","Munchies","Gasoline","Sedating","Toxic"),("","Munchies","Motor Oil","Schizophrenic","Slippery"),("","Munchies","Paracetamol","Anti-gravity","Sneaky"),("","Paranoia","Banana","Jennerising","Gingeritis"),("","Paranoia","Gasoline","Calming","Toxic"),("","Paranoia","Motor Oil","Anti-gravity","Slippery"),("","Paranoia","Paracetamol","Balding","Sneaky"),("","Schizophrenic","Energy Drink","Balding","Athletic"),("","Seizure-Inducing","Horse Semen","Energizing","Long faced"),("","Seizure-Inducing","Mega Bean","Focused","Foggy"),("","Shrinking","Battery","Munchies","Bright-Eyed"),("","Shrinking","Chili","Refreshing","Spicy"),("","Shrinking","Donut","Energizing","Calorie-Dense"),("","Shrinking","Flu Medicine","Paranoia","Sedating"),("","Shrinking","Gasoline","Focused","Toxic"),("","Shrinking","Mega Bean","Electrifying","Foggy"),("","Shrinking","Viagra","Gingeritis","Tropic Thunder"),("","Smelly","Banana","Anti-gravity","Gingeritis"),("Zombifying","","","","")]

class PotionEngine:
    def __init__(self):
        self.base_effects, self.transformations = {}, {}
        for base_ing, base_effect, catalyst, result_effect, catalyst_effect in RECIPES:
            if base_ing: self.base_effects[base_ing] = base_effect
            if catalyst: self.base_effects[catalyst] = catalyst_effect
            if base_effect and catalyst: self.transformations[(base_effect, catalyst)] = (result_effect, catalyst_effect)

    def mix_effects(self, current_effects, ingredient):
        result = list(current_effects)
        if (ingredient_effect := self.base_effects.get(ingredient)):
            for i, effect in enumerate(result):
                if (key := (effect, ingredient)) in self.transformations:
                    new_effect, _ = self.transformations[key]
                    if new_effect not in result: result[i] = new_effect
            if ingredient_effect not in result and len(result) < MAX_EFFECTS:
                result.append(ingredient_effect)
        return sorted(result, key=lambda x: EFFECT_PRIORITIES[x])

def find_recipe(target_effects, initial_effects=None):
    engine = PotionEngine()
    initial = sorted(initial_effects or [], key=lambda x: EFFECT_PRIORITIES[x])
    if set(target_effects).issubset(initial): return []
    seen, queue = {tuple(initial)}, deque([(initial, [])])
    while queue:
        current, recipe = queue.popleft()
        if set(target_effects).issubset(current): return recipe
        for ingredient in engine.base_effects:
            if (mixed := engine.mix_effects(current, ingredient)):
                if len(mixed) <= MAX_EFFECTS and (state := tuple(mixed)) not in seen:
                    seen.add(state)
                    queue.append((mixed, recipe + [ingredient]))
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--desired', required=True, help='Target effects (comma-separated)')
    parser.add_argument('-s', '--starting', default='', help='Initial effects (comma-separated)')
    parser.add_argument('-l', '--list', action='store_true', help='List all effects')
    args = parser.parse_args()

    if args.list:
        for i, effect in enumerate(EFFECTS_SORTED, 1): print(f"{i}: {effect}")
    else:
        parse_effects = lambda x: [e for e in x.strip().replace(',', ' ').split() if e in EFFECTS or (e.isdigit() and (effect:=EFFECTS_SORTED[int(e)-1]))]
        if recipe := find_recipe(parse_effects(args.desired), parse_effects(args.starting)): print(' → '.join(recipe))
        else: print("No solution")