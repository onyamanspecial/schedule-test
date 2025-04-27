#!/usr/bin/env python3
"""
Pathfinder - Find optimal ingredient combinations to achieve desired effects.

This script provides a command-line interface for finding the shortest sequence
of ingredients that will result in having all desired effects active simultaneously,
as well as optimizing drug recipes for maximum profit.
"""

import argparse
from src.data.loader import load_all_data
from src.cli.pathfinder_cli import run_pathfinder
from src.cli.optimizer_cli import setup_optimizer_parser, run_optimizer, CapitalizationHelpFormatter

def main():
    """Main entry point for the pathfinder tool."""
    # Load all required data
    data = load_all_data()
    
    # Setup main command-line argument parser
    parser = argparse.ArgumentParser(
        formatter_class=CapitalizationHelpFormatter,
        description='Pathfinder - Find optimal ingredient combinations and drug recipes',
    )
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Operation mode')
    
    # Pathfinder mode (Mode 1)
    path_parser = subparsers.add_parser(
        '1', 
        help='Find a path to desired effects',
        description='Find a sequence of ingredients to achieve desired effects',
        formatter_class=CapitalizationHelpFormatter
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
        run_pathfinder(args, data)
    
    elif args.mode == '2':
        # Optimizer mode
        run_optimizer(args, data)

if __name__ == "__main__":
    main()