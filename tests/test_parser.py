import pytest
from src.utils.parser import parse_effects

# Sample data for testing
EFFECTS = ["Calming", "Energizing", "Anti-gravity", "Toxic"]
EFFECTS_SORTED = sorted(EFFECTS)

def test_parse_single_number():
    """Test parsing single effect by number."""
    assert parse_effects(["1"], EFFECTS, EFFECTS_SORTED) == {"Anti-gravity"}
    assert parse_effects(["4"], EFFECTS, EFFECTS_SORTED) == {"Toxic"}

def test_parse_multiple_numbers():
    """Test parsing multiple effects by numbers."""
    # Space-separated
    assert parse_effects(["1", "2"], EFFECTS, EFFECTS_SORTED) == {"Anti-gravity", "Calming"}
    # Comma-separated
    assert parse_effects(["1,2"], EFFECTS, EFFECTS_SORTED) == {"Anti-gravity", "Calming"}

def test_parse_single_name():
    """Test parsing single effect by name."""
    assert parse_effects(["Calming"], EFFECTS, EFFECTS_SORTED) == {"Calming"}
    assert parse_effects(["Anti-gravity"], EFFECTS, EFFECTS_SORTED) == {"Anti-gravity"}

def test_parse_multiple_names():
    """Test parsing multiple effects by names."""
    # Space-separated
    assert parse_effects(["Calming", "Toxic"], EFFECTS, EFFECTS_SORTED) == {"Calming", "Toxic"}
    # Comma-separated
    assert parse_effects(["Calming,Toxic"], EFFECTS, EFFECTS_SORTED) == {"Calming", "Toxic"}

def test_case_insensitive():
    """Test case-insensitive matching."""
    assert parse_effects(["calming"], EFFECTS, EFFECTS_SORTED) == {"Calming"}
    assert parse_effects(["CALMING"], EFFECTS, EFFECTS_SORTED) == {"Calming"}
    assert parse_effects(["CaLmInG"], EFFECTS, EFFECTS_SORTED) == {"Calming"}

def test_mixed_format():
    """Test mixing numbers and names."""
    assert parse_effects(["1", "Toxic"], EFFECTS, EFFECTS_SORTED) == {"Anti-gravity", "Toxic"}
    assert parse_effects(["1,Toxic"], EFFECTS, EFFECTS_SORTED) == {"Anti-gravity", "Toxic"}

def test_invalid_inputs():
    """Test handling of invalid inputs."""
    # Invalid numbers
    assert parse_effects(["0"], EFFECTS, EFFECTS_SORTED) == set()
    assert parse_effects(["5"], EFFECTS, EFFECTS_SORTED) == set()
    # Invalid names
    assert parse_effects(["NonExistent"], EFFECTS, EFFECTS_SORTED) == set()
    # Mixed valid/invalid
    assert parse_effects(["1", "NonExistent"], EFFECTS, EFFECTS_SORTED) == {"Anti-gravity"} 