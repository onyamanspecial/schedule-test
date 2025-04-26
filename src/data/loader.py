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

def load_drug_types_data():
    """Load drug types configuration from YAML file.
    
    Returns:
        Tuple containing:
        - List of drug types
        - Dictionary of marijuana strains with their effects and costs
        - List of meth qualities
        - List of quality names
        - List of quality costs
    """
    with open(Path('data/drug_types.yaml'), 'r') as f:
        data = yaml.safe_load(f)
    
    # Extract marijuana strains into a dictionary with tuples (effect, cost)
    strains_data = {}
    for strain, info in data['marijuana_strains'].items():
        strains_data[strain] = (info['effect'], info['base_cost'])
    
    return (
        data['drug_types'],
        strains_data,
        data['meth_qualities'],
        data['quality_names'],
        data['quality_costs']
    )

def load_drug_pricing_data():
    """Load drug pricing configuration from YAML file.
    
    Returns:
        Dictionary containing drug pricing configuration
    """
    with open(Path('data/drug_pricing.yaml'), 'r') as f:
        data = yaml.safe_load(f)
    return data

def load_all_data() -> Tuple[int, List[str], List[str], Dict[str, int], List[Tuple[str, str, str, str, str]], Dict[str, float], Dict[str, int], List[str], Dict[str, Tuple[str, int]], List[int], List[str], List[int], Dict]:
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
        - List of drug types
        - Dictionary of marijuana strains
        - List of meth qualities
        - List of quality names
        - List of quality costs
        - Drug pricing configuration
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
    
    # Load drug types and pricing
    drug_types, strain_data, meth_qualities, quality_names, quality_costs = load_drug_types_data()
    drug_pricing = load_drug_pricing_data()
    
    return max_effects, effects, effects_sorted, effect_priorities, combinations, effect_multipliers, ingredient_prices, drug_types, strain_data, meth_qualities, quality_names, quality_costs, drug_pricing