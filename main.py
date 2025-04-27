#!/usr/bin/env python3

import sys
from src.utils.logger import setup_logger
from src.cli.cli import cli

# Set up logger
logger = setup_logger("pathfinder")

def main():
    """Main entry point for the application."""
    try:
        logger.info("Starting pathfinder application")
        cli()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()