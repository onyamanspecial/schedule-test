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
    return load_all_data()

@pytest.fixture
def mock_args_pathfinder():
    """Create mock arguments for pathfinder CLI."""
    class Args:
        desired = ["Calming", "Energizing"]
        starting = []
        list = False
        
        def __init__(self):
            pass
            
    return Args()

@pytest.fixture
def mock_args_optimizer():
    """Create mock arguments for optimizer CLI."""
    class Args:
        type = 1  # marijuana
        strain = 1  # og_kush
        depth = 3
        grow_tent = False
        pgr = False
        quality = 3  # high quality (for meth)
        
        def __init__(self):
            pass
            
    return Args()

@patch('sys.stdout', new_callable=io.StringIO)
def test_pathfinder_cli_output(mock_stdout, mock_args_pathfinder, data):
    """Test that the pathfinder CLI produces expected output."""
    # Run the pathfinder CLI with mock arguments
    run_pathfinder(mock_args_pathfinder, data)
    
    # Get the output
    output = mock_stdout.getvalue()
    
    # Verify the output contains expected elements
    assert "\u2192" in output, "Output should contain path with arrow symbols"
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
def test_optimizer_cli_different_drug_types(mock_stdout, data):
    """Test that the optimizer CLI handles different drug types."""
    # Test marijuana
    class MarijuanaArgs:
        type = 1  # marijuana
        strain = 1  # og_kush
        depth = 3
        grow_tent = False
        pgr = False
        quality = 3  # not used for marijuana
        
        def __init__(self):
            pass
    
    run_optimizer(MarijuanaArgs(), data)
    marijuana_output = mock_stdout.getvalue()
    mock_stdout.truncate(0)
    mock_stdout.seek(0)
    
    # Test meth
    class MethArgs:
        type = 2  # meth
        strain = 1  # not used for meth
        depth = 3
        grow_tent = False
        pgr = False
        quality = 3  # high quality
        
        def __init__(self):
            pass
    
    run_optimizer(MethArgs(), data)
    meth_output = mock_stdout.getvalue()
    mock_stdout.truncate(0)
    mock_stdout.seek(0)
    
    # Test cocaine
    class CocaineArgs:
        type = 3  # cocaine
        strain = 1  # not used for cocaine
        depth = 3
        grow_tent = False
        pgr = False
        quality = 3  # not used for cocaine
        
        def __init__(self):
            pass
    
    run_optimizer(CocaineArgs(), data)
    cocaine_output = mock_stdout.getvalue()
    
    # Verify each output contains the correct drug type
    assert "marijuana" in marijuana_output, "Output should indicate marijuana"
    assert "meth" in meth_output, "Output should indicate meth"
    assert "cocaine" in cocaine_output, "Output should indicate cocaine"
