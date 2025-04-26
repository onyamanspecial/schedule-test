import argparse
from typing import Dict, List, Any
from src.engine.core import Engine
from src.engine.pathfinder import find_path
from src.utils.parser import parse_effects


def run_pathfinder(args, data):
    """Run the pathfinder with the given arguments and data.
    
    Args:
        args: Parsed command-line arguments
        data: Dictionary containing all loaded data
        
    Returns:
        None, prints results to stdout
    """
    # Extract data
    max_effects = data['max_effects']
    effects = data['effects']
    effects_sorted = data['effects_sorted']
    effect_priorities = data['effect_priorities']
    combinations = data['combinations']
    
    # Handle list mode
    if args.list:
        for i, effect in enumerate(effects_sorted, 1):
            print(f"{i}: {effect}")
        return
    
    # Handle pathfinding mode
    if not args.desired:
        print("Error: The -d/--desired argument is required when not using -l/--list")
        return
    
    # Initialize the engine
    engine = Engine(combinations, max_effects, effect_priorities)
    
    # Parse effect arguments and find path
    if path := find_path(engine,
                       parse_effects(args.desired, effects, effects_sorted),
                       parse_effects(args.starting, effects, effects_sorted)):
        print(' → '.join(path))
    else:
        print("No solution")
