import pytest
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.optimizer import find_best_path

@pytest.fixture
def data():
    """Load all data needed for optimizer tests."""
    return load_all_data()

@pytest.fixture
def engine(data):
    """Create an engine instance with actual data files."""
    return Engine(data['combinations'], data['max_effects'], data['effect_priorities'])

def test_known_profitable_combinations(engine, data):
    """Test specific known-good profitable combinations from the actual data.
    
    These combinations have been verified to work correctly and serve as reference
    test cases. If any of these fail, it means something has changed that
    breaks previously working functionality.
    """
    # Known profitable combinations test cases - each tuple contains:
    # (drug_type, depth, options, expected_path, expected_effects)
    known_combinations = [
        # Marijuana (og_kush) with depth 3
        (
            'marijuana',
            3,
            {'strain': 'og_kush', 'grow_tent': False, 'pgr': False},
            ['Cuke', 'Mega Bean', 'Viagra'],
            ['Foggy', 'Tropic Thunder', 'Glowing', 'Cyclopean']
        ),
        
        # Meth (high quality) with depth 4
        (
            'meth',
            4,
            {'quality': 3},  # High-Quality Pseudo
            ['Banana', 'Cuke', 'Horse Semen', 'Mega Bean'],
            ['Foggy', 'Electrifying', 'Long faced', 'Cyclopean']
        ),
        
        # Cocaine with depth 5
        (
            'cocaine',
            5,
            {},
            ['Banana', 'Cuke', 'Horse Semen', 'Mega Bean', 'Viagra'],
            ['Foggy', 'Tropic Thunder', 'Electrifying', 'Long faced', 'Cyclopean']
        ),
        
        # Marijuana (sour_diesel) with depth 6
        (
            'marijuana',
            6,
            {'strain': 'sour_diesel', 'grow_tent': False, 'pgr': False},
            ['Banana', 'Cuke', 'Horse Semen', 'Mega Bean', 'Iodine', 'Motor Oil'],
            ['Slippery', 'Jennerising', 'Thought-Provoking', 'Electrifying', 'Long faced', 'Anti-gravity', 'Cyclopean']
        )
    ]
    
    for drug_type, depth, options, expected_path, expected_effects in known_combinations:
        # Calculate production cost based on drug type and options
        base_price = data['drug_pricing']['base_prices'][drug_type]
        
        # Set up initial effects based on drug type and options
        initial_effects = []
        if drug_type == 'marijuana':
            strain = options.get('strain', 'og_kush')
            initial_effects = [data['strain_data'][strain][0]]  # Base effect of the strain
        
        # Get grow tent and pgr options
        grow_tent = options.get('grow_tent', False)
        pgr = options.get('pgr', False)
        
        # Calculate production cost
        from src.engine.optimizer import calculate_units, calculate_cost
        units = calculate_units(drug_type, grow_tent, pgr, data['drug_pricing']['production_units'])
        constants = data['drug_pricing']['constants']
        cost_formula = data['drug_pricing']['cost_calculations'][drug_type]['formula']
        
        if drug_type == 'marijuana':
            prod_cost = calculate_cost(
                drug_type, constants, cost_formula,
                strain=options.get('strain', 'og_kush'),
                units=units,
                strain_data=data['strain_data']
            )
        elif drug_type == 'meth':
            prod_cost = calculate_cost(
                drug_type, constants, cost_formula,
                quality=options.get('quality', 3),
                quality_costs=data['quality_costs']
            )
        else:  # cocaine
            prod_cost = calculate_cost(
                drug_type, constants, cost_formula,
                units=units,
                ingredient_prices=data['ingredient_prices']
            )
        
        # Find the best path
        result = find_best_path(
            engine, base_price, prod_cost, depth,
            data['effect_multipliers'], data['ingredient_prices'], data['effect_priorities'],
            initial_effects
        )
        
        assert result is not None, f"No profitable combination found for {drug_type} with depth {depth}"
        effects, path, cost = result
        
        # Verify the path matches expected
        assert path == expected_path, f"""
Path finding result changed for {drug_type} with depth {depth}!
Expected path: {expected_path}
Got instead: {path}
"""
        
        # Verify the effects match expected
        assert set(effects) == set(expected_effects), f"""
Effects changed for {drug_type} with depth {depth}!
Expected effects: {expected_effects}
Got instead: {effects}
"""

def test_profit_calculation(engine, data):
    """Test that profit calculations are correct for known combinations."""
    # Known profitable combinations with expected profits
    profit_test_cases = [
        # (drug_type, depth, options, expected_profit)
        ('marijuana', 3, {'strain': 'og_kush', 'grow_tent': False, 'pgr': False}, 82.83),
        ('meth', 4, {'quality': 3}, 166.00),
        ('cocaine', 5, {}, 466.86),
        ('marijuana', 6, {'strain': 'sour_diesel', 'grow_tent': False, 'pgr': False}, 111.42)
    ]
    
    for drug_type, depth, options, expected_profit in profit_test_cases:
        # Calculate production cost based on drug type and options
        base_price = data['drug_pricing']['base_prices'][drug_type]
        
        # Set up initial effects based on drug type and options
        initial_effects = []
        if drug_type == 'marijuana':
            strain = options.get('strain', 'og_kush')
            initial_effects = [data['strain_data'][strain][0]]  # Base effect of the strain
        
        # Get grow tent and pgr options
        grow_tent = options.get('grow_tent', False)
        pgr = options.get('pgr', False)
        
        # Calculate production cost
        from src.engine.optimizer import calculate_units, calculate_cost
        units = calculate_units(drug_type, grow_tent, pgr, data['drug_pricing']['production_units'])
        constants = data['drug_pricing']['constants']
        cost_formula = data['drug_pricing']['cost_calculations'][drug_type]['formula']
        
        if drug_type == 'marijuana':
            prod_cost = calculate_cost(
                drug_type, constants, cost_formula,
                strain=options.get('strain', 'og_kush'),
                units=units,
                strain_data=data['strain_data']
            )
        elif drug_type == 'meth':
            prod_cost = calculate_cost(
                drug_type, constants, cost_formula,
                quality=options.get('quality', 3),
                quality_costs=data['quality_costs']
            )
        else:  # cocaine
            prod_cost = calculate_cost(
                drug_type, constants, cost_formula,
                units=units,
                ingredient_prices=data['ingredient_prices']
            )
        
        # Find the best path
        result = find_best_path(
            engine, base_price, prod_cost, depth,
            data['effect_multipliers'], data['ingredient_prices'], data['effect_priorities'],
            initial_effects
        )
        
        assert result is not None, f"No profitable combination found for {drug_type} with depth {depth}"
        effects, path, ingredient_cost = result
        
        # Calculate profit
        from src.engine.optimizer import get_effects_value
        total_value = get_effects_value(effects, base_price, data['effect_multipliers'])
        total_cost = prod_cost + ingredient_cost
        profit = total_value - total_cost
        
        # Verify profit is close to expected (allowing for small floating point differences)
        assert abs(profit - expected_profit) < 0.1, f"""
Profit calculation changed for {drug_type} with depth {depth}!
Expected profit: ${expected_profit:.2f}
Got instead: ${profit:.2f}
"""
