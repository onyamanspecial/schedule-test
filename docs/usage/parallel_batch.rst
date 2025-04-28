Parallel Batch Optimizer
=======================

The parallel batch optimizer allows you to process multiple optimizer jobs in parallel, making use of all available CPU cores.

**Workflow:**

1. Place your batch parameter file in `batch_jobs/batch_params.json`.
2. Run the CLI:

   .. code-block:: bash

      python -m src.cli.parallel_optimizer --jobs 4 --batch batch_jobs/batch_params.json

   Results will be saved to `batch_jobs/parallel_optimizer_results.json` by default.

3. You can change the output location with `--results`.

**Where is the logic?**
- Core logic: `src/parallel/batch_optimizer.py`
- CLI entry: `src/cli/parallel_optimizer.py`

**Batch file format:**

.. code-block:: json

   [
     {"drug_type": "meth", "depth": 3, "initial_effects": [], "prod_options": {"quality": 3}},
     {"drug_type": "meth", "depth": 2, "initial_effects": [], "prod_options": {"quality": 2}}
   ]

