# Parallel Batch Optimizer Module

This module contains the core logic for running batch optimizer jobs in parallel, separated from the CLI for maximum reusability.

- Use `run_parallel_batch(batch_path, results_path, jobs)` to run a batch of optimizer jobs in parallel (use `batch_params_optimizer.json`).
- For pathfinder jobs, use your pathfinder batch runner (with `batch_params_pathfinder.json`).
- See `../cli/parallel_optimizer.py` for CLI usage.
