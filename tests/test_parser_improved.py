import pytest
from src.utils.parser import parse_effects

@pytest.mark.parametrize("input_args, expected", [
    (["1"], {"Anti-gravity"}),
    (["4"], {"Toxic"}),
    (["1", "2"], {"Anti-gravity", "Calming"}),
    (["1,2"], {"Anti-gravity", "Calming"}),
    (["Calming"], {"Calming"}),
    (["calming"], {"Calming"}),
    (["CALMING"], {"Calming"}),
    (["1", "Toxic"], {"Anti-gravity", "Toxic"}),
    (["0"], set()),
    (["5"], set()),
    (["NonExistent"], set()),
])
def test_parse_effects(input_args, expected, sample_effects, sample_effects_sorted):
    """Test parsing effects with various inputs using parameterized tests."""
    assert parse_effects(input_args, sample_effects, sample_effects_sorted) == expected

@pytest.mark.parametrize("input_args, expected_count", [
    (["1,2,3,4"], 4),  # All valid effects
    (["1,2,NonExistent"], 2),  # Some valid, some invalid
    (["NonExistent1,NonExistent2"], 0),  # All invalid
])
def test_parse_effects_count(input_args, expected_count, sample_effects, sample_effects_sorted):
    """Test that parse_effects returns the correct number of effects."""
    result = parse_effects(input_args, sample_effects, sample_effects_sorted)
    assert len(result) == expected_count, f"Expected {expected_count} effects, got {len(result)}: {result}"

@pytest.mark.parametrize("effect_name, expected_in_result", [
    ("Calming", True),
    ("calming", True),  # Case-insensitive
    ("CALMING", True),  # Case-insensitive
    ("NonExistent", False),
])
def test_parse_effects_case_insensitive(effect_name, expected_in_result, sample_effects, sample_effects_sorted):
    """Test that parse_effects handles case-insensitive matching correctly."""
    result = parse_effects([effect_name], sample_effects, sample_effects_sorted)
    if expected_in_result:
        assert "Calming" in result, f"Expected 'Calming' in result, got {result}"
    else:
        assert not result, f"Expected empty result, got {result}"
