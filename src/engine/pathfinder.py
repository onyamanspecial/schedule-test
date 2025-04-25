from collections import deque
from typing import List, Optional, Set, Tuple, Deque
from .core import Engine

def find_path(engine: Engine, target_effects: List[str], initial_effects: Optional[List[str]] = None) -> Optional[List[str]]:
    """Find the shortest sequence of ingredients to achieve target effects.
    
    Uses a breadth-first search algorithm to find the shortest path of ingredients
    that will result in having all target effects active simultaneously.
    
    Args:
        engine: Engine instance containing combination rules
        target_effects: List of effects we want to achieve
        initial_effects: Optional list of effects to start with
    
    Returns:
        List of ingredients to combine in sequence, or None if no solution exists
    """
    # Initialize with empty or provided effects, sorted by priority
    initial = sorted(initial_effects or [], key=lambda x: engine.effect_priorities[x])
    
    # Check if we already have all target effects
    if set(target_effects).issubset(initial):
        return []
    
    # Setup for BFS
    seen: Set[Tuple[str, ...]] = {tuple(initial)}
    queue: Deque[Tuple[List[str], List[str]]] = deque([(initial, [])])
    
    # BFS through possible combinations
    while queue:
        current_effects, path = queue.popleft()
        
        # Check if we've found a solution
        if set(target_effects).issubset(current_effects):
            return path
        
        # Try each possible ingredient
        for ingredient in engine.base_effects:
            if result := engine.combine(current_effects, ingredient):
                # Only proceed if within effect limit and haven't seen this state
                if (len(result) <= engine.max_effects and 
                    (state := tuple(result)) not in seen):
                    seen.add(state)
                    queue.append((result, path + [ingredient]))
    
    # No solution found
    return None 