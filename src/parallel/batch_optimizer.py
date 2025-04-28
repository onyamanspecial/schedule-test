import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Any
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.optimizer import find_best_path, calculate_cost, calculate_units, get_effects_value

def run_optimizer_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a single optimizer task with given parameters.
    """
    data = load_all_data()
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    drug_type = params['drug_type']
    depth = params.get('depth', 3)
    initial_effects = params.get('initial_effects', [])
    prod_options = params.get('prod_options', {})

    # Calculate production cost
    units = calculate_units(
        drug_type,
        prod_options.get('grow_tent', False),
        prod_options.get('pgr', False),
        data['drug_pricing']['production_units']
    )
    constants = data['drug_pricing']['constants']
    cost_formula = data['drug_pricing']['cost_calculations'][drug_type]['formula']
    kwargs = {'units': units}
    if drug_type == 'marijuana':
        kwargs.update({
            'strain': prod_options.get('strain', 'og_kush'),
            'strain_data': data['strain_data']
        })
    elif drug_type == 'meth':
        kwargs.update({
            'quality': prod_options.get('quality', 3),
            'quality_costs': data['quality_costs']
        })
    elif drug_type == 'cocaine':
        kwargs.update({
            'ingredient_prices': data['ingredient_prices']
        })
    prod_cost = calculate_cost(drug_type, constants, cost_formula, **kwargs)
    base_price = data['drug_pricing']['base_prices'][drug_type]

    # Run optimizer
    result = find_best_path(
        engine,
        base_price,
        prod_cost,
        depth,
        data['effect_multipliers'],
        data['ingredient_prices'],
        data['effect_priorities'],
        initial_effects
    )

    if not result:
        return {'status': 'no_result', 'params': params}
    effects, path, ingredient_cost = result
    total_value = get_effects_value(effects, base_price, data['effect_multipliers'])
    total_cost = prod_cost + ingredient_cost
    profit = total_value - total_cost
    return {
        'status': 'ok',
        'params': params,
        'effects': effects,
        'path': path,
        'ingredient_cost': ingredient_cost,
        'production_cost': prod_cost,
        'base_price': base_price,
        'total_value': total_value,
        'total_cost': total_cost,
        'profit': profit
    }

def run_parallel_batch(batch_path: str, results_path: str, jobs: int = 4):
    """
    Run multiple optimizer jobs in parallel from a batch JSON file.
    Args:
        batch_path: Path to the JSON file with parameter sets.
        results_path: Path to save the JSON results.
        jobs: Number of parallel worker processes.
    """
    with open(batch_path, 'r') as f:
        batch_params = json.load(f)
    print(f"Running {len(batch_params)} optimizer jobs in parallel (max {jobs} workers)...")

    results = []
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        futures = [executor.submit(run_optimizer_task, p) for p in batch_params]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result['status'] == 'ok':
                print(f"[DONE] {result['params']} -> Profit: ${result['profit']:.2f}, Recipe: {' → '.join(result['path'])}")
            else:
                print(f"[FAIL] {result['params']} -> No result found.")

    # Format floats to 2 decimal places for relevant fields in each result
    for result in results:
        if result.get('status') == 'ok':
            for key in ['ingredient_cost', 'production_cost', 'total_cost', 'profit']:
                if key in result:
                    result[key] = round(result[key], 2)
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"All results saved to {results_path}")
