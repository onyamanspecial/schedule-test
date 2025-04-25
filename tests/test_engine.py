import pytest
from src.engine.core import Engine

# Test data
EFFECTS = ["Calming", "Energizing", "Anti-gravity", "Toxic"]
EFFECT_PRIORITIES = {effect: i for i, effect in enumerate(EFFECTS)}
MAX_EFFECTS = 3

# Sample combinations:
# - Base1 gives Calming
# - Base2 gives Energizing
# - When Calming + Base2 -> Anti-gravity
COMBINATIONS = [
    ("Base1", "Calming", "", "", ""),
    ("Base2", "Energizing", "", "", ""),
    ("", "Calming", "Base2", "Anti-gravity", "Energizing")
]

@pytest.fixture
def engine():
    """Create a test engine instance."""
    return Engine(COMBINATIONS, MAX_EFFECTS, EFFECT_PRIORITIES)

def test_base_effects(engine):
    """Test that ingredients give their base effects."""
    assert engine.combine([], "Base1") == ["Calming"]
    assert engine.combine([], "Base2") == ["Energizing"]

def test_effect_limit(engine):
    """Test that max effects limit is respected."""
    # Add effects up to limit
    result = []
    for _ in range(MAX_EFFECTS):
        result = engine.combine(result, "Base1")
    assert len(result) == 1  # Same effect doesn't stack
    
    # Try to exceed limit
    result = engine.combine(result, "Base2")
    assert len(result) == 2  # Should still be under limit

def test_effect_transformation(engine):
    """Test that effects transform correctly when combined."""
    # Start with Calming
    effects = engine.combine([], "Base1")
    assert effects == ["Calming"]
    
    # Add Base2 - should transform Calming to Anti-gravity
    effects = engine.combine(effects, "Base2")
    assert "Anti-gravity" in effects
    assert "Calming" not in effects
    assert "Energizing" in effects

def test_effect_sorting(engine):
    """Test that effects are sorted by priority."""
    # Add effects in reverse priority order
    effects = engine.combine([], "Base2")  # Energizing
    effects = engine.combine(effects, "Base1")  # Calming
    
    # Should be sorted by priority (based on EFFECTS order)
    assert effects == ["Calming", "Energizing"] 