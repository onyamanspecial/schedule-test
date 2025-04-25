import pytest
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.pathfinder import find_path
from src.utils.parser import parse_effects

@pytest.fixture
def engine():
    """Create an engine instance with actual data files."""
    MAX_EFFECTS, EFFECTS, EFFECTS_SORTED, EFFECT_PRIORITIES, COMBINATIONS = load_all_data()
    return Engine(COMBINATIONS, MAX_EFFECTS, EFFECT_PRIORITIES), EFFECTS, EFFECTS_SORTED

def test_known_paths(engine):
    """Test specific known-good paths from the actual data.
    
    These paths have been verified to work correctly and serve as reference
    test cases. If any of these fail, it means something has changed that
    breaks previously working functionality.
    """
    engine_instance, effects, effects_sorted = engine
    
    # Known path test cases - each tuple contains:
    # (desired effects, starting effects, expected path)
    known_paths = [
        # Complex path with multiple effects and starting effect
        (
            ["23", "21", "9", "10", "12"],  # Bright-eyed, Spicy, Munchies, Refreshing, Sedating
            ["11"],                         # Starting with Focused
            ["Addy", "Flu Medicine", "Iodine", "Mega Bean", "Addy", "Horse Semen"]
        ),
        
        # Simple sequential effects (1,2,3)
        (
            ["1", "2", "3"],               # First three effects
            [],                            # No starting effects
            ["Flu Medicine", "Energy Drink", "Paracetamol", "Mouth Wash"]
        ),
        
        # Using effect names directly
        (
            ["Calming", "Energizing", "Toxic"],
            [],
            ["Addy", "Paracetamol", "Motor Oil", "Mega Bean"]
        ),
        
        # Comma-separated numbers with starting effect
        (
            ["15", "16", "17"],           # Balding, Calorie-Dense, Sneaky
            ["14"],                       # Starting with Laxative
            ["Flu Medicine", "Energy Drink", "Donut", "Mega Bean", "Iodine"]
        ),
        
        # Complex effects with transformation
        (
            ["Anti-gravity", "Glowing"],
            ["Energizing"],
            ["Mega Bean", "Battery", "Iodine", "Motor Oil"]
        )
    ]
    
    for desired, starting, expected_path in known_paths:
        # Convert effect numbers/names to actual effects
        desired_effects = parse_effects(desired, effects, effects_sorted)
        starting_effects = parse_effects(starting, effects, effects_sorted)
        
        # Find path and verify it matches expected
        path = find_path(engine_instance, list(desired_effects), list(starting_effects))
        assert path == expected_path, f"""
Path finding result changed!
Desired effects: {desired}
Starting effects: {starting}
Expected path: {expected_path}
Got instead: {path}
"""

def test_path_validity(engine):
    """Test that found paths actually produce the desired effects.
    
    This test verifies that following any found path actually results
    in having all the desired effects, regardless of the specific path taken.
    """
    engine_instance, effects, effects_sorted = engine
    
    # Test cases covering different scenarios
    test_cases = [
        # Multiple effects with starting effect
        (["23", "21", "9", "10", "12"], ["11"]),
        # Simple sequential effects
        (["1", "2", "3"], []),
        # Named effects
        (["Calming", "Energizing", "Toxic"], []),
        # Effects with starting condition
        (["15", "16", "17"], ["14"]),
        # Complex transformation
        (["Anti-gravity", "Glowing"], ["Energizing"])
    ]
    
    for desired, starting in test_cases:
        # Convert effect numbers/names to actual effects
        desired_effects = parse_effects(desired, effects, effects_sorted)
        starting_effects = parse_effects(starting, effects, effects_sorted)
        
        # Find path
        path = find_path(engine_instance, list(desired_effects), list(starting_effects))
        assert path is not None, f"No path found for {desired} starting with {starting}"
        
        # Follow path and verify we get desired effects
        current_effects = list(starting_effects)
        for ingredient in path:
            current_effects = engine_instance.combine(current_effects, ingredient)
        
        # Verify all desired effects are present
        for effect in desired_effects:
            assert effect in current_effects, f"""
Effect {effect} not achieved!
Desired effects: {desired_effects}
Starting effects: {starting_effects}
Path taken: {path}
Final effects: {current_effects}
""" 