# Pathfinder

A Python-based potion crafting simulator that helps find the shortest path to achieve desired effects by combining different ingredients.

## Features

- Interactive command-line interface
- Support for multiple effects and ingredients
- Real-time progress tracking with ETA
- Clear visualization of mixing steps
- Maximum of 8 effects per potion
- Efficient pathfinding using Breadth-First Search (BFS)

## Usage

Run the script using Python:

```bash
python pathfinder.py
```

Follow the prompts to:
1. Enter desired effects (using IDs or full names)
2. Specify starting effects (if any)
3. View the optimal recipe to achieve your desired effects

Example inputs:
- Using IDs: `1 5 10`
- Using names: `Paranoia Smelly`
- Using underscores: `Tropic_Thunder`

The program will show:
- Available effects with their IDs
- Step-by-step mixing process
- Final recipe with ingredients in order

Press Ctrl+C to interrupt the search at any time.

## Requirements

- Python 3.x
- Standard Python libraries (no additional dependencies needed) 