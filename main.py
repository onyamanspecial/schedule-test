#!/usr/bin/env python3
"""
Pathfinder - Find optimal ingredient combinations to achieve desired effects.

This script provides a command-line interface for finding the shortest sequence
of ingredients that will result in having all desired effects active simultaneously,
as well as optimizing drug recipes for maximum profit.
"""

import argparse
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.pathfinder import find_path
from src.engine.optimizer.cli import setup_optimizer_parser, run_optimizer
from src.utils.parser import parse_effects

def main():
    """Main entry point for the pathfinder tool."""
    # Load all required data
    data = {}
    (
        data['max_effects'], data['effects'], data['effects_sorted'], 
        data['effect_priorities'], data['combinations'], data['effect_multipliers'], 
        data['ingredient_prices'], data['drug_types'], data['strain_data'], 
        data['meth_qualities'], data['quality_names'], data['quality_costs'], 
        data['drug_pricing']
    ) = load_all_data()
    
    # Setup main command-line argument parser
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30, width=80),
        description='Pathfinder - Find optimal ingredient combinations and drug recipes',
    )
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Operation mode')
    
    # Pathfinder mode (Mode 1)
    path_parser = subparsers.add_parser(
        '1', 
        help='Find a path to desired effects',
        description='Find a sequence of ingredients to achieve desired effects'
    )
    path_parser.add_argument('-d', '--desired', metavar='EFFECTS', nargs='+',
                       help='Specify effects to achieve (names or numbers, comma-separated or space-separated)')
    path_parser.add_argument('-s', '--starting', metavar='EFFECTS', nargs='*', default=[],
                       help='Start with these effects (optional, comma-separated or space-separated)')
    path_parser.add_argument('-l', '--list', action='store_true',
                       help='List all available effects with their numbers')
    
    # Optimizer mode (Mode 2)
    optimize_parser = setup_optimizer_parser(subparsers)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle different modes
    if not args.mode:
        # Show help when no mode is specified
        parser.print_help()
        return
        
    if args.mode == '1':
        # Pathfinder mode
        if args.list:
            # List all effects
            for i, effect in enumerate(data['effects_sorted'], 1):
                print(f"{i}: {effect}")
        elif not args.desired:
            path_parser.error('The -d/--desired argument is required when not using -l/--list')
        else:
            # Initialize the engine
            engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
            
            # Parse effect arguments and find path
            if path := find_path(engine,
                           parse_effects(args.desired, data['effects'], data['effects_sorted']),
                           parse_effects(args.starting, data['effects'], data['effects_sorted'])):
                print(' → '.join(path))
            else:
                print("No solution")
    
    elif args.mode == '2':
        # Optimizer mode
        run_optimizer(args, data)

if __name__ == "__main__":
    main()