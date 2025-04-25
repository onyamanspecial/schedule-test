from typing import List, Set

def parse_effects(args: List[str], effects: List[str], effects_sorted: List[str]) -> Set[str]:
    """Parse effect arguments into a set of valid effects.
    
    Args:
        args: List of arguments that may contain effect names or numbers
        effects: List of all valid effects
        effects_sorted: Sorted list of effects for index lookup
    
    Returns:
        Set of valid effects found in the arguments
    """
    result = set()
    parts = []
    for arg in args:
        parts.extend(part.strip() for part in arg.split(',') if part.strip())
    
    for part in parts:
        try:
            idx = int(part)
            if 1 <= idx <= len(effects_sorted):
                result.add(effects_sorted[idx - 1])
            continue
        except ValueError:
            pass
        
        if part in effects:
            result.add(part)
            continue
            
        matches = [e for e in effects if e.lower() == part.lower()]
        if matches:
            result.add(matches[0])
            continue
            
        if ' ' in part:
            if part in effects:
                result.add(part)
                continue
            matches = [e for e in effects if e.lower() == part.lower()]
            if matches:
                result.add(matches[0])
    
    return result 