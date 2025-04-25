# Pathfinder

A command-line tool for finding optimal ingredient combinations to achieve desired effects. Uses a breadth-first search algorithm to find the shortest path to desired effects.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pathfinder.git
cd pathfinder

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py [-h] [-d EFFECTS ...] [-s EFFECTS ...] [-l]
```

### Options

- `-d, --desired EFFECTS`  : Effects to achieve (required unless using -l)
- `-s, --starting EFFECTS` : Starting effects (optional)
- `-l, --list`            : List all available effects with their numbers
- `-h, --help`            : Show help message

### Input Formats

Effects can be specified in several ways:
- By number: `1`, `2`, `3` (use `-l` to see numbers)
- By name: `"Calming"`, `"Anti-gravity"`
- Multiple effects:
  ```bash
  # Space-separated numbers
  python main.py -d 1 2 3

  # Comma-separated numbers
  python main.py -d 1,2,3

  # Space-separated names
  python main.py -d "Calming" "Energizing"

  # Comma-separated names
  python main.py -d "Calming,Energizing"
  ```

### Examples

List all available effects:
```bash
python main.py -l
```

Find path to single effect:
```bash
# By name
python main.py -d "Calming"

# By number
python main.py -d 3
```

Find path to multiple effects:
```bash
# By name
python main.py -d "Calming" "Energizing"

# By number
python main.py -d 3,11
```

Find path with starting effects:
```bash
# Start with Energizing, find path to Anti-gravity
python main.py -d "Anti-gravity" -s "Energizing"

# Start with effect 11, find path to effects 23,21,9
python main.py -d 23,21,9 -s 11
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
python -m pytest tests/test_integration.py
```

The test suite includes:
- Integration tests that verify complete paths with real data
- Parser tests for input validation and processing
- Comprehensive test cases with known working combinations
- Validation of effect transformations and complex paths

## Project Structure

```
pathfinder/
├── data/                 # Data files
│   ├── effects.yaml      # Available effects and max limit
│   └── combinations.yaml # Ingredient combinations and their effects
├── src/                  # Source code
│   ├── data/            # Data management
│   │   └── loader.py    # YAML file loading and processing
│   ├── engine/          # Core algorithms
│   │   ├── core.py      # Effect combination logic
│   │   └── pathfinder.py # Path finding algorithm
│   └── utils/           # Helper functions
│       └── parser.py    # Command-line argument parsing
├── tests/               # Test suite
│   ├── test_integration.py # End-to-end tests with real data
│   └── test_parser.py   # Input parsing tests
├── main.py              # Command-line interface
└── requirements.txt     # Dependencies
```

## Requirements

- Python ≥ 3.9
- PyYAML ≥ 6.0.1 (for reading configuration files) 