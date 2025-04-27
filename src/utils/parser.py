from typing import List, Set

def parse_effects(args: List[str], effects: List[str], effects_sorted: List[str]) -> Set[str]:
    """Parse command-line arguments into a set of valid effects.
    
    Args:
        args: List of effect names or numbers from command line
        effects: List of all valid effect names
        effects_sorted: List of effects sorted by priority
        
    Returns:
        Set of valid effect names
    """
    result = set()
    
    # Process all arguments and split any comma-separated values
    parts = []
    for arg in args:
        parts.extend(part.strip() for part in arg.split(',') if part.strip())
    
    for part in parts:
        # Try to parse as a number first
        try:
            effect_index = int(part) - 1  # Convert to 0-based index
            if 0 <= effect_index < len(effects_sorted):
                result.add(effects_sorted[effect_index])
            continue
        except ValueError:
            pass
        
        # Try as an exact effect name
        if part in effects:
            result.add(part)
            continue
        
        # Try case-insensitive matching
        for effect in effects:
            if effect.lower() == part.lower():
                result.add(effect)
                break
    
    return result