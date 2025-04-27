import click
from typing import List, Set
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.utils.parser import parse_effects
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)

@click.group()
def cli():
    """Pathfinder - A tool for finding optimal paths and combinations."""
    pass

@cli.command()
@click.option('--desired', '-d', help='Desired effects to achieve (comma-separated)')
@click.option('--starting', '-s', default='', help='Starting effects (comma-separated)')
@click.option('--list', '-l', is_flag=True, help='List all available effects')
def pathfinder(desired, starting, list):
    """Find paths to desired effects."""
    logger.info("Starting pathfinder mode")
    
    # Load data
    data = load_all_data()
    
    # List effects if requested
    if list:
        click.echo("\nAvailable effects:")
        for i, effect in enumerate(data['effects_sorted'], 1):
            click.echo(f"{i}. {effect}")
        return
    
    # Check if desired effects are specified
    if not desired:
        click.echo("Error: No desired effects specified.")
        click.echo("Use --list to see available effects.")
        return
    
    # Parse effects
    desired_list = [desired]
    starting_list = [starting] if starting else []
    
    desired_effects = parse_effects(desired_list, data['effects'], data['effects_sorted'])
    starting_effects = parse_effects(starting_list, data['effects'], data['effects_sorted'])
    
    # Create engine
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    
    # Manual implementation of find_path to avoid import issues
    path = find_path_manual(engine, list(desired_effects), list(starting_effects))
    
    # Check if path was found
    if not path:
        click.echo("No solution found.")
        return
    
    # Calculate final effects
    current_effects = list(starting_effects)
    for ingredient in path:
        current_effects = engine.combine(current_effects, ingredient)
    
    # Print results
    click.echo(f"\nPath: {' → '.join(path)}")
    click.echo("\nAchieved effects:")
    for effect in sorted(current_effects, key=lambda x: x.lower()):
        marker = "*" if effect in desired_effects else " "
        click.echo(f"{marker} {effect}")
    
    click.echo(f"\nTotal ingredients: {len(path)}")
    click.echo(f"Total effects: {len(current_effects)}")
    click.echo(f"Desired effects achieved: {len(set(current_effects) & desired_effects)} / {len(desired_effects)}")

@cli.command()
@click.option('--type', '-t', type=click.Choice(['1', '2', '3']), required=True,
              help='Drug type: 1=marijuana, 2=meth, 3=cocaine')
@click.option('--depth', '-d', type=int, default=3,
              help='Maximum search depth (number of ingredients to add)')
@click.option('--grow-tent', '-g', is_flag=True, help='Use a grow tent')
@click.option('--pgr', '-p', is_flag=True, help='Use plant growth regulators')
@click.option('--strain', '-s', type=int, help='Strain for marijuana (1-5)')
@click.option('--quality', '-q', type=int, help='Quality for meth (1-3)')
def optimizer(type, depth, grow_tent, pgr, strain, quality):
    """Find the most profitable drug combinations."""
    logger.info("Starting optimizer mode")
    
    # Load data
    data = load_all_data()
    
    # Get drug type
    type_idx = int(type) - 1
    drug_types = data['drug_types']
    drug_type = drug_types[type_idx]
    
    # Set up initial effects
    initial_effects = []
    
    # Handle drug-specific options
    if drug_type == 'marijuana':
        if not strain:
            strain = 1
        strains = list(data['strain_data'].keys())
        strain_name = strains[strain - 1]
        initial_effects = [data['strain_data'][strain_name][0]]
        click.echo(f"Using marijuana strain: {strain_name}")
    elif drug_type == 'meth':
        if not quality:
            quality = 3
        click.echo(f"Using meth quality: {quality}")
    
    # Import optimizer functions here to avoid circular imports
    from src.engine.optimizer import find_best_path, calculate_units, calculate_cost, get_effects_value
    
    # Calculate production cost
    constants = data['drug_pricing']['constants']
    cost_formula = data['drug_pricing']['cost_calculations'][drug_type]['formula']
    units = calculate_units(drug_type, grow_tent, pgr, data['drug_pricing']['production_units'])
    
    # Set up cost calculation arguments
    kwargs = {'units': units}
    
    if drug_type == 'marijuana':
        kwargs.update({
            'strain': strain_name,
            'strain_data': data['strain_data']
        })
    elif drug_type == 'meth':
        kwargs.update({
            'quality': quality,
            'quality_costs': data['quality_costs']
        })
    elif drug_type == 'cocaine':
        kwargs.update({
            'ingredient_prices': data['ingredient_prices']
        })
    
    # Calculate production cost
    prod_cost = calculate_cost(drug_type, constants, cost_formula, **kwargs)
    
    # Get base price
    base_price = data['drug_pricing']['base_prices'][drug_type]
    
    # Create engine
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    
    # Find best path
    result = find_best_path(
        engine, base_price, prod_cost, depth,
        data['effect_multipliers'], data['ingredient_prices'], data['effect_priorities'],
        initial_effects
    )
    
    # Check if a profitable combination was found
    if not result:
        click.echo(f"No profitable combination found for {drug_type} with depth {depth}")
        return
    
    # Unpack result
    effects, path, ingredient_cost = result
    
    # Calculate value and profit
    total_value = get_effects_value(effects, base_price, data['effect_multipliers'])
    total_cost = prod_cost + ingredient_cost
    profit = total_value - total_cost
    
    # Print results
    click.echo(f"\nBest Combination for {drug_type}:")
    click.echo(f"Production Cost: ${prod_cost:.2f}")
    click.echo(f"Ingredients: {', '.join(path)}")
    click.echo(f"Ingredient Cost: ${ingredient_cost:.2f}")
    click.echo(f"Total Cost: ${total_cost:.2f}")
    click.echo(f"Total Value: ${total_value:.2f}")
    click.echo(f"Profit: ${profit:.2f}")
    click.echo(f"Effects: {', '.join(effects)}")
    click.echo(f"Recipe: {' → '.join(path)}")

def find_path_manual(engine: Engine, target_effects: List[str], initial_effects: List[str] = None) -> List[str]:
    """Find the shortest sequence of ingredients to achieve target effects.
    
    Args:
        engine: Engine instance containing combination rules
        target_effects: List of effects we want to achieve
        initial_effects: Optional list of effects to start with
        
    Returns:
        List of ingredients to combine in sequence, or None if no solution exists
    """
    from collections import deque
    
    # Initialize with empty or provided effects, sorted by priority
    initial = sorted(initial_effects or [], key=lambda x: engine.effect_priorities[x])
    
    # Check if we already have all target effects
    if set(target_effects).issubset(initial):
        return []
    
    # Setup for BFS
    seen = {tuple(initial)}
    queue = deque([(initial, [])])
    
    # BFS through possible combinations
    while queue:
        current_effects, path = queue.popleft()
        
        # Check if we've found a solution
        if set(target_effects).issubset(current_effects):
            return path
        
        # Try each possible ingredient
        for ingredient in engine.base_effects:
            # Get the result of combining current effects with this ingredient
            result = engine.combine(current_effects, ingredient)
            
            # Only proceed if we have results and within effect limit and haven't seen this state
            if result and len(result) <= engine.max_effects:
                state = tuple(sorted(result))
                if state not in seen:
                    seen.add(state)
                    queue.append((result, path + [ingredient]))
    
    # No solution found
    return None

if __name__ == '__main__':
    cli()
