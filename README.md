# Pathfinder

A command-line tool for finding optimal ingredient combinations to achieve desired effects. The tool has two main functionalities:

1. **Pathfinder**: Find the shortest path to achieve desired effects using a breadth-first search algorithm
2. **Optimizer**: Find the most profitable drug recipe based on effects and ingredient costs

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pathfinder.git
cd pathfinder

# Install dependencies
pip install -r requirements.txt
```

## Usage

The application has two operation modes, selected by the first positional argument:

```bash
python main.py {1,2} [options]
```

### Mode 1: Pathfinder

Find the shortest path to achieve desired effects:

```bash
python main.py 1 [-h] [-d EFFECTS ...] [-s EFFECTS ...] [-l]
```

#### Pathfinder Options

- `-d, --desired EFFECTS`  : Effects to achieve (required unless using -l)
- `-s, --starting EFFECTS` : Starting effects (optional)
- `-l, --list`            : List all available effects with their numbers
- `-h, --help`            : Show help message

### Mode 2: Optimizer

Find the most profitable drug recipe:

```bash
python main.py 2 [-h] -t N [-d N] [-g] [-p] [-s N] [-q {1,2,3}]
```

#### Optimizer Options

- `-t, --type N`       : Drug type (1=marijuana, 2=meth, 3=cocaine) [required]
- `-d, --depth N`      : Search depth (default: 3)
- `-g, --grow-tent`    : Use grow tent
- `-p, --pgr`          : Use plant growth regulators
- `-s, --strain N`     : Strain for marijuana (1=og_kush, 2=sour_diesel, etc.)
- `-q, --quality {1,2,3}` : Quality for meth (1=low, 2=medium, 3=high)

### Input Formats for Pathfinder

Effects can be specified in several ways:
- By number: `1`, `2`, `3` (use `-l` to see numbers)
- By name: `"Calming"`, `"Anti-gravity"`
- Multiple effects:
  ```bash
  # Space-separated numbers
  python main.py 1 -d 1 2 3

  # Comma-separated numbers
  python main.py 1 -d 1,2,3

  # Space-separated names
  python main.py 1 -d "Calming" "Energizing"

  # Comma-separated names
  python main.py 1 -d "Calming,Energizing"
  ```

### Examples

#### Pathfinder Examples

List all available effects:
```bash
python main.py 1 -l
```

Find path to single effect:
```bash
# By name
python main.py 1 -d "Calming"

# By number
python main.py 1 -d 3
```

Find path to multiple effects:
```bash
# By name
python main.py 1 -d "Calming" "Energizing"

# By number
python main.py 1 -d 3,11
```

Find path with starting effects:
```bash
# Start with Energizing, find path to Anti-gravity
python main.py 1 -d "Anti-gravity" -s "Energizing"

# Start with effect 11, find path to effects 23,21,9
python main.py 1 -d 23,21,9 -s 11
```

#### Optimizer Examples

Find the most profitable marijuana recipe:
```bash
python main.py 2 -t 1 -s 1 -d 3
```

Find the most profitable meth recipe with high quality:
```bash
python main.py 2 -t 2 -q 3 -d 4
```

Find the most profitable cocaine recipe with grow tent:
```bash
python main.py 2 -t 3 -g -d 5
```

## Development

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_pathfinder_consistency.py
```

The test suite includes:
- Pathfinder consistency tests that verify complete paths with real data
- Optimizer consistency tests that verify profitable combinations
- CLI tests for command-line interface functionality
- Parser tests for input validation and processing
- Core engine tests for effect transformations and combinations

## Project Structure

```
pathfinder/
├── data/                       # Configuration data in YAML files
│   ├── combinations.yaml       # Ingredient combinations and their effects
│   ├── drug_pricing.yaml       # Drug pricing and production costs
│   ├── drug_types.yaml         # Drug types and their properties
│   ├── effect_multipliers.yaml # Effect value multipliers
│   ├── effects.yaml            # Available effects and max limit
│   └── ingredient_prices.yaml  # Ingredient costs
├── src/                        # Source code
│   ├── cli/                    # Command-line interface modules
│   │   ├── optimizer_cli.py    # Optimizer CLI functionality
│   │   └── pathfinder_cli.py   # Pathfinder CLI functionality
│   ├── data/                   # Data management
│   │   └── loader.py           # YAML file loading and processing
│   ├── engine/                 # Core algorithms
│   │   ├── core.py             # Effect combination logic
│   │   ├── optimizer.py        # Optimizer algorithms
│   │   └── pathfinder.py       # Path finding algorithm
│   └── utils/                  # Helper functions
│       └── parser.py           # Command-line argument parsing
├── tests/                      # Test suite
│   ├── test_cli.py             # CLI tests
│   ├── test_engine.py          # Core engine tests
│   ├── test_optimizer_consistency.py # Optimizer consistency tests
│   ├── test_parser.py          # Input parsing tests
│   └── test_pathfinder_consistency.py # Pathfinder consistency tests
├── main.py                     # Main entry point with CLI
└── requirements.txt            # Dependencies
```

## Requirements

- Python ≥ 3.9
- PyYAML ≥ 6.0.1 (for reading configuration files)