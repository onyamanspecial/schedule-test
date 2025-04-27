import pytest
from src.data.loader import load_all_data
from src.engine.core import Engine

@pytest.fixture(scope="session")
def test_data():
    """Load test data once for all tests."""
    return load_all_data()

@pytest.fixture
def mock_engine(test_data):
    """Create a mock engine with test data."""
    return Engine(
        test_data["combinations"],
        test_data["max_effects"],
        test_data["effect_priorities"]
    )

@pytest.fixture
def sample_effects():
    """Sample effects for testing."""
    return ["Calming", "Energizing", "Anti-gravity", "Toxic"]

@pytest.fixture
def sample_effects_sorted(sample_effects):
    """Sample effects sorted for testing."""
    return sorted(sample_effects)

@pytest.fixture
def sample_effect_priorities(sample_effects):
    """Sample effect priorities for testing."""
    return {effect: i+1 for i, effect in enumerate(sample_effects)}

@pytest.fixture
def sample_combinations():
    """Sample combinations for testing."""
    return [
        ("Mega Bean", "Foggy", "Paracetamol", "Calming", "Sneaky"),
        ("Paracetamol", "Sneaky", "Addy", "Thought-Provoking", "Energizing"),
        ("Addy", "Energizing", "Mega Bean", "Glowing", "Foggy"),
    ]

@pytest.fixture
def sample_engine(sample_combinations, sample_effect_priorities):
    """Create a sample engine with test data."""
    return Engine(
        sample_combinations,
        8,  # max_effects
        sample_effect_priorities
    )
