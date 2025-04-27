from collections import deque
from typing import List, Dict, Tuple, Optional

class Engine:
    """Core engine for handling effect combinations and transformations.
    
    This class manages the combination rules between ingredients and their effects,
    including how effects transform when combined with certain ingredients.
    
    Attributes:
        max_effects: Maximum number of effects that can be active at once
        effect_priorities: Dictionary mapping effects to their priority (for sorting)
        base_effects: Dictionary mapping ingredients to their base effects
        transforms: Dictionary mapping (effect, ingredient) pairs to their transformation results
    """
    
    def __init__(self, combinations: List[Tuple[str, str, str, str, str]], 
                 max_effects: int, effect_priorities: Dict[str, int]):
        """Initialize the engine with combination rules and constraints.
        
        Args:
            combinations: List of (base, base_effect, modifier, result_effect, mod_effect) tuples
            max_effects: Maximum number of effects that can be active at once
            effect_priorities: Dictionary mapping effects to their sort priority
        """
        self.max_effects = max_effects
        self.effect_priorities = effect_priorities
        self.base_effects = {}
        self.transforms = {}
        
        # Process each combination rule
        for base, base_effect, modifier, result_effect, mod_effect in combinations:
            # Store base effects for ingredients
            if base: self.base_effects[base] = base_effect
            if modifier: self.base_effects[modifier] = mod_effect
            # Store transformation rules
            if base_effect and modifier: 
                self.transforms[(base_effect, modifier)] = (result_effect, mod_effect)

    def combine(self, effects: List[str], ingredient: str) -> List[str]:
        """Combine current effects with a new ingredient.
        
        Args:
            effects: Current list of active effects
            ingredient: New ingredient to add
            
        Returns:
            New list of effects after combining with the ingredient,
            sorted by effect priority
        """
        result = list(effects)
        
        # Only process if ingredient has a base effect
        ingredient_effect = self.base_effects.get(ingredient)
        if ingredient_effect:
            # Check for transformations with existing effects
            for idx, effect in enumerate(result):
                key = (effect, ingredient)
                if key in self.transforms:
                    new_effect = self.transforms[key][0]
                    if new_effect not in result:
                        result[idx] = new_effect
            
            # Add ingredient's base effect if space allows
            if ingredient_effect not in result and len(result) < self.max_effects:
                result.append(ingredient_effect)
        
        # Sort by effect priority
        return sorted(result, key=lambda x: self.effect_priorities[x]) 