"""
CLI entry point for running batch optimizer jobs in parallel.

Usage:
    python -m src.cli.parallel_optimizer --jobs 4 --batch batch_jobs/batch_params.json

This script delegates the core logic to src.parallel.batch_optimizer for maintainability.
Results will be saved to batch_jobs/parallel_optimizer_results.json by default.
"""
import argparse
import os
from src.parallel.batch_optimizer import run_parallel_batch

def main():
    parser = argparse.ArgumentParser(description='Parallel Drug Optimizer CLI')
    parser.add_argument('--jobs', type=int, default=4, help='Number of parallel jobs')
    parser.add_argument('--batch', type=str, required=True, help='Path to batch parameter JSON file')
    parser.add_argument('--results', type=str, default=None, help='Path to save results JSON file (default: in same dir as batch)')
    args = parser.parse_args()

    batch_path = args.batch
    results_path = args.results or os.path.join(os.path.dirname(batch_path), 'parallel_optimizer_results.json')

    run_parallel_batch(batch_path, results_path, jobs=args.jobs)

if __name__ == '__main__':
    main()
