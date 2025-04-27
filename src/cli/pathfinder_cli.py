import argparse
from typing import Dict, List, Set, Any, Optional
from src.engine.core import Engine
from src.engine.pathfinder import find_path
from src.utils.parser import parse_effects


def print_effects_list(effects: List[str]) -> None:
    """Print a numbered list of effects.
    
    Args:
        effects: List of effects to print
    """
    print("\nAvailable effects:")
    for i, effect in enumerate(effects, 1):
        print(f"{i}. {effect}")


def print_path_result(path: List[str], effects: Set[str], desired_effects: Set[str]) -> None:
    """Print the result of a pathfinding operation.
    
    Args:
        path: List of ingredients in the path
        effects: Set of effects achieved
        desired_effects: Set of desired effects
    """
    if not path:
        print("No solution found.")
        return
    
    # Print the path
    print(f"\nPath: {' \u2192 '.join(path)}")
    
    # Print achieved effects
    print("\nAchieved effects:")
    # Sort effects to ensure consistent output
    sorted_effects = sorted(effects, key=lambda x: x.lower())
    for effect in sorted_effects:
        marker = "*" if effect in desired_effects else " "
        print(f"{marker} {effect}")
    
    # Print stats
    print(f"\nTotal ingredients: {len(path)}")
    print(f"Total effects: {len(effects)}")
    print(f"Desired effects achieved: {len(effects.intersection(desired_effects))} / {len(desired_effects)}")


def run_pathfinder(args, data: Dict[str, Any]) -> None:
    """Run the pathfinder with the given arguments.
    
    Args:
        args: Command-line arguments
        data: Dictionary containing all loaded data
    """
    # If list mode is enabled, just print the effects list and exit
    if args.list:
        print_effects_list(data['effects_sorted'])
        return
    
    # Parse desired and starting effects
    desired_effects = parse_effects(args.desired, data['effects'], data['effects_sorted'])
    starting_effects = parse_effects(args.starting, data['effects'], data['effects_sorted'])
    
    # Validate that we have desired effects
    if not desired_effects:
        print("Error: No valid desired effects specified.")
        print("Use --list to see available effects or check your input.")
        return
    
    # Create the engine
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    
    # Find the path
    path = find_path(engine, desired_effects, starting_effects)
    
    # If we found a path, determine the final effects
    if path:
        # Track effects at each step to ensure accuracy
        current_effects = list(starting_effects)
        for ingredient in path:
            current_effects = engine.combine(current_effects, ingredient)
        final_effects = set(current_effects)  # Convert to set for the print_path_result function
    else:
        final_effects = set()
        print("No solution found.")
    
    # Print the result only if we found a path
    if path:
        print_path_result(path, final_effects, desired_effects)


def setup_pathfinder_parser(subparsers) -> None:
    """Set up the command-line parser for the pathfinder.
    
    Args:
        subparsers: Subparsers object from argparse
    """
    parser = subparsers.add_parser('pathfinder', help='Find paths to desired effects')
    
    parser.add_argument('--desired', nargs='+', default=[],
                        help='Desired effects to achieve (names or numbers)')
    parser.add_argument('--starting', nargs='+', default=[],
                        help='Starting effects (names or numbers)')
    parser.add_argument('--list', action='store_true',
                        help='List all available effects')
