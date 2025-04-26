#!/usr/bin/env python3
"""
Drug Optimizer - Find optimal ingredient combinations to maximize profit.

This script provides a command-line interface for finding the most profitable
sequence of ingredients to add to different drug types.
"""

import argparse
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.optimizer import find_best_path, calculate_units, calculate_cost, get_effects_value
from src.cli.optimizer_cli import create_parser, run_optimizer

def main():
    """Main entry point for the drug optimizer tool."""
    # Load all required data
    MAX_EFFECTS, EFFECTS, EFFECTS_SORTED, EFFECT_PRIORITIES, RULES_DATA, EFFECT_MULTIPLIERS, INGREDIENT_PRICES, \
    DRUG_TYPES, STRAIN_DATA, METH_QUALITIES, QUALITY_NAMES, QUALITY_COSTS, DRUG_PRICING = load_all_data()
    
    # Initialize the engine
    engine = Engine(RULES_DATA, MAX_EFFECTS, EFFECT_PRIORITIES)
    
    # Parse command-line arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Run the optimizer
    run_optimizer(
        DRUG_TYPES, STRAIN_DATA, QUALITY_NAMES, QUALITY_COSTS, DRUG_PRICING,
        engine, EFFECT_PRIORITIES, INGREDIENT_PRICES, EFFECT_MULTIPLIERS, args
    )

if __name__ == "__main__":
    main()
