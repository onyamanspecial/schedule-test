from typing import Dict, List, Set, Any, Callable
import sys
import time
from threading import Thread
from queue import Queue

def format_list(items: List[str], prefix: str = "") -> str:
    """Format a list of items for display.
    
    Args:
        items: List of items to format
        prefix: Optional prefix for each item
        
    Returns:
        Formatted string
    """
    return "\n".join(f"{prefix}{item}" for item in items)

def print_table(headers: List[str], rows: List[List[Any]], padding: int = 2) -> None:
    """Print a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of rows, each containing values for each column
        padding: Padding between columns
    """
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Print headers
    header_row = " ".join(h.ljust(widths[i] + padding) for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))
    
    # Print rows
    for row in rows:
        print(" ".join(str(cell).ljust(widths[i] + padding) for i, cell in enumerate(row)))

def process_effects(engine, path: List[str], starting_effects: List[str]) -> List[str]:
    """Process a sequence of ingredients to determine final effects.
    
    Args:
        engine: Engine instance
        path: List of ingredients to process
        starting_effects: Initial effects
        
    Returns:
        List of final effects
    """
    current_effects = list(starting_effects)
    for ingredient in path:
        current_effects = engine.combine(current_effects, ingredient)
    return current_effects

def execute_with_progress(func: Callable, *args, **kwargs) -> Any:
    """Execute a function with a progress indicator.
    
    Args:
        func: Function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        Result of the function
    """
    start_time = time.time()
    spinner = "|/-\\"
    i = 0
    
    # Start a background thread to execute the function
    result_queue = Queue()
    
    def worker():
        try:
            result = func(*args, **kwargs)
            result_queue.put(("success", result))
        except Exception as e:
            result_queue.put(("error", e))
    
    thread = Thread(target=worker)
    thread.start()
    
    # Show spinner while waiting
    while thread.is_alive():
        sys.stdout.write(f"\rProcessing {spinner[i % len(spinner)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    
    # Get result
    status, result = result_queue.get()
    elapsed = time.time() - start_time
    
    sys.stdout.write(f"\rCompleted in {elapsed:.2f}s{'.' + ' ' * 20}\n")
    
    if status == "error":
        raise result
    
    return result

def format_path(path: List[str]) -> str:
    """Format a path of ingredients with arrow separators.
    
    Args:
        path: List of ingredients in the path
        
    Returns:
        Formatted path string
    """
    return " \u2192 ".join(path)

def format_effects(effects: List[str], desired_effects: Set[str] = None) -> str:
    """Format a list of effects, marking desired effects with an asterisk.
    
    Args:
        effects: List of effects to format
        desired_effects: Optional set of desired effects to mark
        
    Returns:
        Formatted effects string
    """
    if desired_effects is None:
        desired_effects = set()
    
    result = []
    for effect in sorted(effects, key=lambda x: x.lower()):
        marker = "*" if effect in desired_effects else " "
        result.append(f"{marker} {effect}")
    
    return "\n".join(result)
