from collections import deque
from math import floor
from typing import Dict, List, Tuple, Optional, Any


def get_effects_value(effects: List[str], base_price: float, effect_multipliers: Dict[str, float]) -> int:
    """Calculate the value of a drug based on its effects and base price.
    
    Args:
        effects: List of active effects
        base_price: Base price of the drug
        effect_multipliers: Dictionary mapping effects to their value multipliers
        
    Returns:
        The calculated value of the drug
    """
    return floor(base_price * (1 + sum(effect_multipliers.get(e, 0) for e in effects)))


def find_best_path(engine, base_price: float, prod_cost: float, max_depth: int, 
                  effect_multipliers: Dict[str, float], ingredient_prices: Dict[str, int],
                  effect_priorities: Dict[str, int], initial: Optional[List[str]] = None) -> Tuple[List[str], List[str], float]:
    """Find the most profitable combination of ingredients.
    
    Uses a breadth-first search algorithm to find the most profitable combination
    of ingredients that maximizes the value of the drug.
    
    Args:
        engine: Engine instance containing combination rules
        base_price: Base price of the drug
        prod_cost: Production cost per unit
        max_depth: Maximum search depth (number of ingredients to add)
        effect_multipliers: Dictionary mapping effects to their value multipliers
        ingredient_prices: Dictionary mapping ingredients to their prices
        effect_priorities: Dictionary mapping effects to their sort priorities
        initial: Optional list of effects to start with
        
    Returns:
        Tuple containing:
        - List of effects in the optimal combination
        - List of ingredients to combine in sequence
        - Total cost of the ingredients
    """
    queue = deque([(0, 0.0, tuple(sorted(initial or [], key=lambda x: effect_priorities[x])), [])])
    visited = {}
    best_profit, best_state = float('-inf'), None
    
    while queue:
        depth, cost, effects, path = queue.popleft()
        profit = get_effects_value(effects, base_price, effect_multipliers) - (prod_cost + cost)
        
        if profit > best_profit:
            best_profit, best_state = profit, (effects, path, cost)
            
        if depth < max_depth:
            for ing in engine.base_effects:
                new_effects = engine.combine(list(effects), ing)
                new_eff = tuple(new_effects)
                new_cost = cost + ingredient_prices.get(ing, 0)
                
                if new_eff not in visited or new_cost < visited[new_eff][0] or profit > visited[new_eff][1]:
                    visited[new_eff] = (new_cost, profit)
                    queue.append((depth+1, new_cost, new_eff, path+[ing]))
                    
    return best_state


def calculate_units(drug_type: str, grow_tent: bool, pgr: bool, production_units: Dict[str, Any]) -> int:
    """Calculate production units based on configuration.
    
    Args:
        drug_type: Type of drug being produced
        grow_tent: Whether a grow tent is being used
        pgr: Whether plant growth regulators are being used
        production_units: Dictionary containing production unit configurations
        
    Returns:
        Number of units produced
    """
    unit_config = production_units.get(drug_type)
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


def calculate_marijuana_cost(constants: Dict[str, Any], strain: str, units: int, 
                           strain_data: Dict[str, Tuple[str, int]]) -> float:
    """Calculate production cost for marijuana.
    
    Args:
        constants: Dictionary containing constants for calculations
        strain: Selected marijuana strain
        units: Number of units produced
        strain_data: Dictionary mapping strains to their effects and costs
        
    Returns:
        Production cost per unit
    """
    seed_cost = strain_data[strain][1]  # Get the base cost of the strain
    soil_cost_per_seed = constants['plant_soil_cost'] / constants['plant_soil_uses']
    total_per_seed = seed_cost + soil_cost_per_seed
    return total_per_seed / units


def calculate_meth_cost(constants: Dict[str, Any], quality: int, 
                      quality_costs: List[int]) -> float:
    """Calculate production cost for meth.
    
    Args:
        constants: Dictionary containing constants for calculations
        quality: Selected meth quality (1-3)
        quality_costs: List of costs for different meth qualities
        
    Returns:
        Production cost per unit
    """
    pseudo_cost = quality_costs[quality-1]
    total_batch_cost = pseudo_cost + constants['meth_acid_cost'] + constants['meth_phosphorus_cost']
    return total_batch_cost / constants['meth_batch_size']


def calculate_cocaine_cost(constants: Dict[str, Any], units: int,
                         ingredient_prices: Dict[str, int]) -> float:
    """Calculate production cost for cocaine.
    
    Args:
        constants: Dictionary containing constants for calculations
        units: Number of units produced
        ingredient_prices: Dictionary mapping ingredients to their prices
        
    Returns:
        Production cost per unit
    """
    soil_cost_per_seed = constants['plant_soil_cost'] / constants['plant_soil_uses']
    seed_cost = constants['cocaine_seed_cost']
    total_per_seed = seed_cost + soil_cost_per_seed
    gasoline_cost = ingredient_prices['Gasoline'] * constants['gasoline_per_cocaine_unit']
    return (total_per_seed / units) + gasoline_cost


def calculate_cost(drug_type: str, constants: Dict[str, Any], cost_formula: str, 
                  **kwargs) -> float:
    """Calculate production cost based on configuration.
    
    Args:
        drug_type: Type of drug being produced
        constants: Dictionary containing constants for calculations
        cost_formula: Formula to use for calculation
        **kwargs: Additional keyword arguments needed for specific drug types
        
    Returns:
        Production cost per unit
    """
    if cost_formula == 'soil_and_seed':
        return calculate_marijuana_cost(
            constants, 
            kwargs.get('strain', ''), 
            kwargs.get('units', 1), 
            kwargs.get('strain_data', {})
        )
    
    elif cost_formula == 'batch_based':
        return calculate_meth_cost(
            constants, 
            kwargs.get('quality', 3), 
            kwargs.get('quality_costs', [])
        )
    
    elif cost_formula == 'seed_and_gasoline':
        return calculate_cocaine_cost(
            constants, 
            kwargs.get('units', 1), 
            kwargs.get('ingredient_prices', {})
        )
    
    return 0  # Default fallback
