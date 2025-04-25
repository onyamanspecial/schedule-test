import pytest
from src.engine.core import Engine
from src.engine.pathfinder import find_path

# Test data
EFFECTS = ["Calming", "Energizing", "Anti-gravity", "Toxic"]
EFFECT_PRIORITIES = {effect: i for i, effect in enumerate(EFFECTS)}
MAX_EFFECTS = 3

# Sample combinations that form a known path:
# Base1 -> Calming
# Base2 -> Energizing
# Calming + Base2 -> Anti-gravity + Energizing
COMBINATIONS = [
    ("Base1", "Calming", "", "", ""),
    ("Base2", "Energizing", "", "", ""),
    ("", "Calming", "Base2", "Anti-gravity", "Energizing")
]

@pytest.fixture
def engine():
    """Create a test engine instance."""
    return Engine(COMBINATIONS, MAX_EFFECTS, EFFECT_PRIORITIES)

def test_single_effect_path(engine):
    """Test finding path to a single effect."""
    # Path to Calming
    path = find_path(engine, ["Calming"])
    assert path == ["Base1"]
    
    # Path to Energizing
    path = find_path(engine, ["Energizing"])
    assert path == ["Base2"]

def test_multiple_effects_path(engine):
    """Test finding path to multiple effects."""
    # Path to both Calming and Energizing
    path = find_path(engine, ["Calming", "Energizing"])
    assert path == ["Base1", "Base2"]

def test_transformation_path(engine):
    """Test finding path that requires effect transformation."""
    # Path to Anti-gravity (requires Calming + Base2)
    path = find_path(engine, ["Anti-gravity"])
    assert path == ["Base1", "Base2"]

def test_impossible_path(engine):
    """Test handling of impossible effect combinations."""
    # No way to get Toxic
    path = find_path(engine, ["Toxic"])
    assert path is None
    
    # Can't have Anti-gravity and Calming (transformation removes Calming)
    path = find_path(engine, ["Anti-gravity", "Calming"])
    assert path is None

def test_starting_effects(engine):
    """Test pathfinding with initial effects."""
    # Starting with Calming, find path to Anti-gravity
    path = find_path(engine, ["Anti-gravity"], ["Calming"])
    assert path == ["Base2"]
    
    # Starting with effect we want
    path = find_path(engine, ["Calming"], ["Calming"])
    assert path == [] 