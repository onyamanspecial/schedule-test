from collections import deque
from math import floor
from typing import Dict, List, Tuple, Optional, Any

def get_effects_value(effects: List[str], base_price: int, effect_multipliers: Dict[str, float]) -> int:
    """Calculate the value of a drug based on its effects and base price.
    
    Args:
        effects: List of active effects
        base_price: Base price of the drug
        effect_multipliers: Dictionary mapping effects to their value multipliers
        
    Returns:
        The calculated value of the drug
    """
    return floor(base_price * (1 + sum(effect_multipliers.get(e, 0) for e in effects)))

def find_best_path(engine, base_price: int, prod_cost: float, max_depth: int, 
                  effect_priorities: Dict[str, int], ingredient_prices: Dict[str, int],
                  effect_multipliers: Dict[str, float], initial: Optional[List[str]] = None) -> Tuple[Tuple[str, ...], List[str], float]:
    """Find the most profitable combination of ingredients.
    
    Uses a breadth-first search algorithm to find the combination of ingredients
    that will result in the highest profit.
    
    Args:
        engine: Engine instance containing combination rules
        base_price: Base price of the drug
        prod_cost: Production cost per unit
        max_depth: Maximum number of ingredients to add
        effect_priorities: Dictionary mapping effects to their sort priorities
        ingredient_prices: Dictionary mapping ingredients to their prices
        effect_multipliers: Dictionary mapping effects to their value multipliers
        initial: Optional list of effects to start with
        
    Returns:
        Tuple containing:
        - Tuple of final effects
        - List of ingredients to combine in sequence
        - Total cost of ingredients
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

# Helper function to calculate production units based on configuration
def calculate_units(drug_type: str, grow_tent: bool, pgr: bool, production_units: Dict[str, Any]) -> int:
    """Calculate the number of units produced based on production configuration.
    
    Args:
        drug_type: Type of drug being produced
        grow_tent: Whether a grow tent is being used
        pgr: Whether plant growth regulators are being used
        production_units: Production units configuration dictionary
        
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

# Helper function to calculate production cost based on configuration
def calculate_cost(drug_type: str, constants: Dict[str, Any], cost_calculations: Dict[str, Any],
                  strain_data: Dict[str, Tuple[str, int]], quality_costs: List[int],
                  ingredient_prices: Dict[str, int], strain: Optional[str] = None, 
                  quality: Optional[int] = None, units: Optional[int] = None) -> float:
    """Calculate the production cost of a drug.
    
    Args:
        drug_type: Type of drug being produced
        constants: Dictionary of constant values for calculations
        cost_calculations: Cost calculation formulas configuration
        strain_data: Dictionary mapping marijuana strains to their effects and costs
        quality_costs: List of costs for different meth qualities
        ingredient_prices: Dictionary mapping ingredients to their prices
        strain: Optional strain of marijuana
        quality: Optional quality level of meth
        units: Optional number of units produced
        
    Returns:
        Production cost per unit
    """
    formula = cost_calculations.get(drug_type, {}).get('formula')
    
    if formula == 'soil_and_seed':
        # Marijuana: (seed_cost + soil_cost_per_seed) / units_per_seed
        if strain and units:
            seed_cost = strain_data[strain][1]  # Get the base cost of the strain
            soil_cost_per_seed = constants['plant_soil_cost'] / constants['plant_soil_uses']
            total_per_seed = seed_cost + soil_cost_per_seed
            return total_per_seed / units
    
    elif formula == 'batch_based':
        # Meth: (pseudo_cost + meth_acid_cost + meth_phosphorus_cost) / meth_batch_size
        if quality is not None:
            pseudo_cost = quality_costs[quality-1]
            total_batch_cost = pseudo_cost + constants['meth_acid_cost'] + constants['meth_phosphorus_cost']
            return total_batch_cost / constants['meth_batch_size']
    
    elif formula == 'seed_and_gasoline':
        # Cocaine: (seed_cost + soil_cost_per_seed) / units_per_seed + gasoline_cost
        if units:
            soil_cost_per_seed = constants['plant_soil_cost'] / constants['plant_soil_uses']
            seed_cost = constants['cocaine_seed_cost']
            total_per_seed = seed_cost + soil_cost_per_seed
            gasoline_cost = ingredient_prices['Gasoline'] * constants['gasoline_per_cocaine_unit']
            return (total_per_seed / units) + gasoline_cost
    
    return 0  # Default fallback
