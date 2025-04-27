import click
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.pathfinder import find_path
from src.engine.optimizer import find_best_path, calculate_units, calculate_cost
from src.utils.parser import parse_effects
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)

@click.group()
def cli():
    """Pathfinder - A tool for finding optimal paths and combinations."""
    pass

@cli.command()
@click.option('--desired', '-d', multiple=True, help='Desired effects to achieve (names or numbers)')
@click.option('--starting', '-s', multiple=True, help='Starting effects (names or numbers)')
@click.option('--list', '-l', is_flag=True, help='List all available effects')
def pathfinder(desired, starting, list):
    """Find paths to desired effects."""
    logger.info("Starting pathfinder mode")
    data = load_all_data()
    
    if list:
        click.echo("\nAvailable effects:")
        for i, effect in enumerate(data['effects_sorted'], 1):
            click.echo(f"{i}. {effect}")
        return
    
    if not desired:
        click.echo("Error: No desired effects specified.")
        click.echo("Use --list to see available effects.")
        return
    
    desired_effects = parse_effects(desired, data['effects'], data['effects_sorted'])
    starting_effects = parse_effects(starting, data['effects'], data['effects_sorted'])
    
    logger.info(f"Searching for path to achieve {desired_effects} starting with {starting_effects}")
    
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    path = find_path(engine, desired_effects, starting_effects)
    
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
@click.option('--type', '-t', type=click.Choice(['1', '2', '3']), default='1',
              help='Drug type: 1=marijuana, 2=meth, 3=cocaine')
@click.option('--strain', '-s', type=click.IntRange(1, 5), default=1,
              help='Marijuana strain: 1=og_kush, 2=sour_diesel, 3=purple_haze, 4=white_widow, 5=blue_dream')
@click.option('--depth', '-d', type=int, default=3,
              help='Maximum search depth (number of ingredients to add)')
@click.option('--grow-tent', is_flag=True, help='Use a grow tent for marijuana or cocaine')
@click.option('--pgr', is_flag=True, help='Use plant growth regulators for marijuana or cocaine')
@click.option('--quality', '-q', type=click.IntRange(1, 3), default=3,
              help='Meth quality: 1=low, 2=medium, 3=high')
def optimizer(type, strain, depth, grow_tent, pgr, quality):
    """Find the most profitable drug combinations."""
    logger.info("Starting optimizer mode")
    data = load_all_data()
    
    # Convert type to int and get drug type
    type_idx = int(type) - 1
    drug_types = data['drug_types']
    drug_type = drug_types[type_idx]
    
    logger.info(f"Optimizing for {drug_type} with depth {depth}")
    
    # Set up options based on drug type
    initial_effects = []
    options = {
        'grow_tent': grow_tent,
        'pgr': pgr
    }
    
    if drug_type == 'marijuana':
        # Get strain information
        strains = list(data['strain_data'].keys())
        strain_name = strains[strain - 1]
        initial_effects = [data['strain_data'][strain_name][0]]
        options['strain'] = strain_name
        logger.info(f"Using marijuana strain: {strain_name}")
    elif drug_type == 'meth':
        options['quality'] = quality
        logger.info(f"Using meth quality: {quality}")
    
    # Calculate production cost
    constants = data['drug_pricing']['constants']
    cost_formula = data['drug_pricing']['cost_calculations'][drug_type]['formula']
    units = calculate_units(drug_type, grow_tent, pgr, data['drug_pricing']['production_units'])
    
    # Set up kwargs for cost calculation
    kwargs = {'units': units}
    
    if drug_type == 'marijuana':
        kwargs.update({
            'strain': options.get('strain', 'og_kush'),
            'strain_data': data['strain_data']
        })
    elif drug_type == 'meth':
        kwargs.update({
            'quality': options.get('quality', 3),
            'quality_costs': data['quality_costs']
        })
    elif drug_type == 'cocaine':
        kwargs.update({
            'ingredient_prices': data['ingredient_prices']
        })
    
    # Calculate the production cost
    prod_cost = calculate_cost(drug_type, constants, cost_formula, **kwargs)
    
    # Get base price for the drug
    base_price = data['drug_pricing']['base_prices'][drug_type]
    
    # Create engine
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    
    # Find the best path
    result = find_best_path(
        engine, base_price, prod_cost, depth,
        data['effect_multipliers'], data['ingredient_prices'], data['effect_priorities'],
        initial_effects
    )
    
    if not result:
        click.echo(f"No profitable combination found for {drug_type} with depth {depth}")
        return
    
    effects, path, ingredient_cost = result
    
    # Calculate value and profit
    from src.engine.optimizer import get_effects_value
    total_value = get_effects_value(effects, base_price, data['effect_multipliers'])
    total_cost = prod_cost + ingredient_cost
    profit = total_value - total_cost
    
    # Print the results
    click.echo(f"\nBest Combination for {drug_type}:")
    click.echo(f"Production Cost: ${prod_cost:.2f}")
    click.echo(f"Ingredients: {', '.join(path)}")
    click.echo(f"Ingredient Cost: ${ingredient_cost:.2f}")
    click.echo(f"Total Cost: ${total_cost:.2f}")
    click.echo(f"Total Value: ${total_value:.2f}")
    click.echo(f"Profit: ${profit:.2f}")
    click.echo(f"Effects: {', '.join(effects)}")
    click.echo(f"Recipe: {' → '.join(path)}")

if __name__ == '__main__':
    cli()
