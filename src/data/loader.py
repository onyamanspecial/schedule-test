import yaml
from pathlib import Path
from typing import List, Dict, Tuple

def load_effects_data() -> Tuple[int, List[str]]:
    """Load effects configuration from YAML file.
    
    Returns:
        Tuple containing:
        - Maximum number of effects allowed simultaneously
        - List of all possible effects
    """
    with open(Path('data/effects.yaml'), 'r') as f:
        data = yaml.safe_load(f)
    return int(data['max_effects']), list(data['effects'])

def load_effect_multipliers() -> Dict[str, float]:
    """Load effect multipliers from YAML file.
    
    Returns:
        Dictionary mapping effect names to their value multipliers
    """
    with open(Path('data/effect_multipliers.yaml'), 'r') as f:
        data = yaml.safe_load(f)
    return dict(data['effect_multipliers'])

def load_ingredient_prices() -> Dict[str, int]:
    """Load ingredient prices from YAML file.
    
    Returns:
        Dictionary mapping ingredient names to their prices
    """
    with open(Path('data/ingredient_prices.yaml'), 'r') as f:
        data = yaml.safe_load(f)
    return dict(data['ingredient_prices'])

def load_combinations_data() -> List[Tuple[str, str, str, str, str]]:
    """Load ingredient combinations and their effects from YAML file.
    
    Returns:
        List of tuples, each containing:
        - base: Base ingredient name
        - base_effect: Effect of the base ingredient
        - modifier: Modifier ingredient name
        - result_effect: Effect after combination
        - modifier_effect: Effect of the modifier ingredient
    """
    with open(Path('data/combinations.yaml'), 'r') as f:
        data = yaml.safe_load(f)
    return [(str(item.get('base', '')), str(item.get('base_effect', '')), 
             str(item.get('modifier', '')), str(item.get('result_effect', '')), 
             str(item.get('modifier_effect', ''))) for item in data['combinations']]

def get_effect_priorities(effects: List[str]) -> Dict[str, int]:
    """Create a mapping of effects to their sort priorities.
    
    Args:
        effects: List of all possible effects
        
    Returns:
        Dictionary mapping each effect to its index in the list
    """
    return {effect: idx for idx, effect in enumerate(effects)}

def load_all_data() -> Tuple[int, List[str], List[str], Dict[str, int], List[Tuple[str, str, str, str, str]], Dict[str, float], Dict[str, int]]:
    """Load and process all required data.
    
    Returns:
        Tuple containing:
        - Maximum effects allowed
        - List of all effects
        - Sorted list of effects
        - Effect priority mapping
        - List of ingredient combinations
        - Effect multipliers dictionary
        - Ingredient prices dictionary
    """
    # Load base data
    max_effects, effects = load_effects_data()
    
    # Create sorted list and priorities
    effects_sorted = sorted(effects)
    effect_priorities = get_effect_priorities(effects)
    
    # Load combinations
    combinations = load_combinations_data()
    
    # Load multipliers and prices
    effect_multipliers = load_effect_multipliers()
    ingredient_prices = load_ingredient_prices()
    
    return max_effects, effects, effects_sorted, effect_priorities, combinations, effect_multipliers, ingredient_prices