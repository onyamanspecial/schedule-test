#!/usr/bin/env python3
"""
Pathfinder - Find optimal ingredient combinations to achieve desired effects.

This script provides a command-line interface for finding the shortest sequence
of ingredients that will result in having all desired effects active simultaneously.
"""

import argparse
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.pathfinder import find_path
from src.utils.parser import parse_effects

def main():
    """Main entry point for the pathfinder tool."""
    # Load all required data
    MAX_EFFECTS, EFFECTS, EFFECTS_SORTED, EFFECT_PRIORITIES, COMBINATIONS = load_all_data()
    
    # Initialize the engine
    engine = Engine(COMBINATIONS, MAX_EFFECTS, EFFECT_PRIORITIES)

    # Setup command-line argument parser
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30, width=80),
        description='Find a sequence of ingredients to achieve desired effects',
        usage='%(prog)s -d EFFECTS [-s EFFECTS] [-l]'
    )
    parser.add_argument('-d', '--desired', metavar='EFFECTS', nargs='+',
                       help='Specify effects to achieve (names or numbers, comma-separated or space-separated)')
    parser.add_argument('-s', '--starting', metavar='EFFECTS', nargs='*', default=[],
                       help='Start with these effects (optional, comma-separated or space-separated)')
    parser.add_argument('-l', '--list', action='store_true',
                       help='List all available effects with their numbers')
    
    # Parse arguments
    args = parser.parse_args()

    # Handle list mode
    if args.list:
        for i, effect in enumerate(EFFECTS_SORTED, 1):
            print(f"{i}: {effect}")
    
    # Handle pathfinding mode
    elif not args.desired:
        parser.error('The -d/--desired argument is required when not using -l/--list')
    else:
        # Parse effect arguments and find path
        if path := find_path(engine,
                           parse_effects(args.desired, EFFECTS, EFFECTS_SORTED),
                           parse_effects(args.starting, EFFECTS, EFFECTS_SORTED)):
            print(' → '.join(path))
        else:
            print("No solution")

if __name__ == "__main__":
    main() 