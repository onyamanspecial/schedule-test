"""
Batch runner for pathfinder jobs.
Reads a JSON file containing a list of pathfinder jobs (desired_effects, initial_effects),
runs each job, and saves the results to a JSON file.
"""
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from src.data.loader import load_all_data
from src.engine.core import Engine
from src.engine.pathfinder import find_path
from src.utils.parser import parse_effects

def process_pathfinder_job(job, data):
    desired_effects = set(job['desired_effects'])
    initial_effects = set(job.get('initial_effects', []))
    engine = Engine(data['combinations'], data['max_effects'], data['effect_priorities'])
    path = find_path(engine, desired_effects, initial_effects)
    if path:
        current_effects = list(initial_effects)
        for ingredient in path:
            current_effects = engine.combine(current_effects, ingredient)
        final_effects = set(current_effects)
        return {
            'status': 'ok',
            'params': job,
            'effects': sorted(list(final_effects)),
            'path': path
        }
    else:
        return {
            'status': 'fail',
            'params': job,
            'reason': 'No solution found.'
        }

def run_batch_pathfinder(batch_path: str, results_path: str = None, jobs: int = 4):
    with open(batch_path, 'r') as f:
        batch_jobs = json.load(f)
    data = load_all_data()
    results = []
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        futures = [executor.submit(process_pathfinder_job, job, data) for job in batch_jobs]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    if results_path is None:
        results_path = os.path.join(os.path.dirname(batch_path), 'parallel_pathfinder_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"All pathfinder results saved to {results_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Batch Pathfinder Runner')
    parser.add_argument('--batch', type=str, required=True, help='Path to batch parameter JSON file')
    parser.add_argument('--results', type=str, default=None, help='Path to save results JSON file (default: in same dir as batch)')
    parser.add_argument('--jobs', type=int, default=4, help='Number of parallel worker processes (default: 4)')
    args = parser.parse_args()
    run_batch_pathfinder(args.batch, args.results, jobs=args.jobs)
