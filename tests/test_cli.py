import pytest
import sys
import io
from unittest.mock import patch
from src.cli.pathfinder_cli import run_pathfinder
from src.cli.optimizer_cli import run_optimizer
from src.data.loader import load_all_data

@pytest.fixture
def data():
    """Load all data needed for CLI tests."""
    # Convert tuple to dictionary for easier access
    raw_data = load_all_data()
    data_dict = {
        'max_effects': raw_data[0],
        'effects': raw_data[1],
        'effects_sorted': raw_data[2],
        'effect_priorities': raw_data[3],
        'combinations': raw_data[4],
        'effect_multipliers': raw_data[5],
        'ingredient_prices': raw_data[6],
        'drug_types': raw_data[7],
        'strain_data': raw_data[8],
        'meth_qualities': raw_data[9],
        'quality_names': raw_data[10],
        'quality_costs': raw_data[11],
        'drug_pricing': raw_data[12]
    }
    return data_dict

# Create a simple class for mock arguments
class MockArgs:
    """Base class for mock arguments."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@pytest.fixture
def mock_args_pathfinder():
    """Create mock arguments for pathfinder CLI."""
    return MockArgs(
        desired=["Calming", "Energizing"],
        starting=[],
        list=False
    )

@pytest.fixture
def mock_args_optimizer():
    """Create mock arguments for optimizer CLI."""
    return MockArgs(
        type=1,  # marijuana
        strain=1,  # og_kush
        depth=3,
        grow_tent=False,
        pgr=False,
        quality=3  # high quality (for meth)
    )

@patch('sys.stdout', new_callable=io.StringIO)
def test_pathfinder_cli_output(mock_stdout, mock_args_pathfinder, data):
    """Test that the pathfinder CLI produces expected output."""
    # Run the pathfinder CLI with mock arguments
    run_pathfinder(mock_args_pathfinder, data)
    
    # Get the output
    output = mock_stdout.getvalue()
    
    # Verify the output contains expected elements
    assert "→" in output, "Output should contain path with arrow symbols"
    assert not output.isspace(), "Output should not be empty"

@patch('sys.stdout', new_callable=io.StringIO)
def test_optimizer_cli_output(mock_stdout, mock_args_optimizer, data):
    """Test that the optimizer CLI produces expected output."""
    # Run the optimizer CLI with mock arguments
    run_optimizer(mock_args_optimizer, data)
    
    # Get the output
    output = mock_stdout.getvalue()
    
    # Verify the output contains expected elements
    assert "Best Combination for marijuana" in output, "Output should indicate drug type"
    assert "Production Cost:" in output, "Output should show production cost"
    assert "Ingredients" in output, "Output should list ingredients"
    assert "Total Cost:" in output, "Output should show total cost"
    assert "Total Value:" in output, "Output should show total value"
    assert "Profit:" in output, "Output should show profit"
    assert "Effects:" in output, "Output should list effects"
    assert "Recipe:" in output, "Output should show recipe"
    assert not output.isspace(), "Output should not be empty"

@patch('sys.stdout', new_callable=io.StringIO)
def test_pathfinder_cli_no_solution(mock_stdout, data):
    """Test that the pathfinder CLI handles cases with no solution."""
    # Create args with impossible combination of effects
    args = MockArgs(
        desired=["Impossible Effect 1", "Impossible Effect 2"],
        starting=[],
        list=False
    )
    
    # Run the pathfinder CLI with impossible args
    run_pathfinder(args, data)
    
    # Get the output
    output = mock_stdout.getvalue()
    
    # Verify the output indicates no solution
    assert "No solution" in output, "Output should indicate no solution was found"

@patch('sys.stdout', new_callable=io.StringIO)
def test_optimizer_cli_different_drug_types(mock_stdout, data):
    """Test that the optimizer CLI handles different drug types."""
    # Test marijuana
    marijuana_args = MockArgs(
        type=1,  # marijuana
        strain=1,  # og_kush
        depth=3,
        grow_tent=False,
        pgr=False,
        quality=3  # not used for marijuana
    )
    
    run_optimizer(marijuana_args, data)
    marijuana_output = mock_stdout.getvalue()
    mock_stdout.truncate(0)
    mock_stdout.seek(0)
    
    # Test meth
    meth_args = MockArgs(
        type=2,  # meth
        strain=1,  # not used for meth
        depth=3,
        grow_tent=False,
        pgr=False,
        quality=3  # high quality
    )
    
    run_optimizer(meth_args, data)
    meth_output = mock_stdout.getvalue()
    mock_stdout.truncate(0)
    mock_stdout.seek(0)
    
    # Test cocaine
    cocaine_args = MockArgs(
        type=3,  # cocaine
        strain=1,  # not used for cocaine
        depth=3,
        grow_tent=False,
        pgr=False,
        quality=3  # not used for cocaine
    )
    
    run_optimizer(cocaine_args, data)
    cocaine_output = mock_stdout.getvalue()
    
    # Verify each output contains the correct drug type
    assert "marijuana" in marijuana_output, "Output should indicate marijuana"
    assert "meth" in meth_output, "Output should indicate meth"
    assert "cocaine" in cocaine_output, "Output should indicate cocaine"
