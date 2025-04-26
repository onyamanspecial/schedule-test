#!/usr/bin/env python3
"""
Pathfinder - Find optimal ingredient combinations to achieve desired effects.

This script provides a command-line interface for finding the shortest sequence
of ingredients that will result in having all desired effects active simultaneously,
as well as optimizing drug recipes for maximum profit.
"""

import argparse
from src.data.loader import load_all_data
from src.cli.pathfinder_cli import setup_pathfinder_parser, run_pathfinder
from src.cli.optimizer_cli import setup_optimizer_parser, run_optimizer, CapitalizationHelpFormatter

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
        formatter_class=CapitalizationHelpFormatter,
        description='Pathfinder - Find optimal ingredient combinations and drug recipes',
    )
    
    # Add mode flag
    parser.add_argument('-m', '--mode', type=int, choices=[1, 2], required=True,
                      help='Operation mode: 1=pathfinder, 2=optimizer')
    
    # Parse known args first to get the mode
    args, remaining = parser.parse_known_args()
    
    # Reset parser for the selected mode
    if args.mode == 1:
        # Pathfinder mode
        parser = argparse.ArgumentParser(
            formatter_class=CapitalizationHelpFormatter,
            description='Pathfinder - Find a sequence of ingredients to achieve desired effects',
        )
        parser.add_argument('-m', '--mode', type=int, choices=[1], default=1, help=argparse.SUPPRESS)
        setup_pathfinder_parser(parser)
    else:  # args.mode == 2
        # Optimizer mode
        parser = argparse.ArgumentParser(
            formatter_class=CapitalizationHelpFormatter,
            description='Drug Optimizer - Find the most profitable combination of ingredients',
        )
        parser.add_argument('-m', '--mode', type=int, choices=[2], default=2, help=argparse.SUPPRESS)
        setup_optimizer_parser(parser)
    
    # Parse all arguments
    args = parser.parse_args()
    
    # Run the selected mode
    if args.mode == 1:
        run_pathfinder(args, data)
    else:  # args.mode == 2
        run_optimizer(args, data)

if __name__ == "__main__":
    main()