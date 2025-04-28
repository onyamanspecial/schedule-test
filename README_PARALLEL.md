# Parallel Batch Optimizer Usage

## Directory Structure

- `batch_jobs/` — Place your batch parameter JSON files and results here.
- `src/parallel/batch_optimizer.py` — Core logic for running batch optimizer jobs in parallel.
- `src/cli/parallel_optimizer.py` — CLI entry point for batch/parallel optimization.

## Usage

1. **Prepare your batch parameters:**
   - For optimizer jobs, edit `batch_jobs/batch_params_optimizer.json`.
   - For pathfinder jobs, edit `batch_jobs/batch_params_pathfinder.json`.
   - Each batch file should only contain jobs of the appropriate type (see below for details).

   ### Example: Optimizer Job (Economical Mode)
   ```json
   {
     "drug_type": "marijuana",
     "depth": 3,
     "prod_options": { "grow_tent": true, "pgr": false, "strain": "og_kush" }
   }
   ```
   - For marijuana and cocaine, you **must** include a "strain" in prod_options.

   ```json
   {
     "drug_type": "cocaine",
     "depth": 2,
     "prod_options": { "grow_tent": true, "pgr": true, "strain": "og_kush" }
   }
   ```
   - For meth, use the "quality" field in prod_options:
   ```json
   {
     "drug_type": "meth",
     "depth": 4,
     "prod_options": { "quality": 2 }
   }
   ```
   - Do not include effects fields in optimizer jobs.

   ### Example: Pathfinder Job (Effects Mode)
   ```json
   {
     "desired_effects": ["Euphoric", "Focused"]
   }
   ```
   - This job finds a path to achieve the desired effects. Do not include drug_type, prod_options, or depth.

   ### Example: Pathfinder Job With Initial Effects
   ```json
   {
     "desired_effects": ["Sedating"],
     "initial_effects": ["Calming"]
   }
   ```
   - This job tries to transform "Calming" into "Sedating". Do not include drug_type, prod_options, or depth.

   ### Example: Mixed Batch
   ```json
   [
     {
       "drug_type": "marijuana",
       "depth": 3,
       "prod_options": { "grow_tent": true, "pgr": false, "strain": "og_kush" }
     },
     {
       "desired_effects": ["Euphoric"]
     },
     {
       "desired_effects": ["Euphoric", "Focused"],
       "initial_effects": ["Calming"]
     }
   ]
   ```
   - You can include both optimizer and pathfinder jobs in one batch. Each job must follow the correct required/optional fields for its mode.

---

#### Batch Job Modes Cheatsheet
```text
+------------+-------------------------------+--------------------+------------------------------+
|   MODE     |      Required Fields          |  Optional Fields   |      Ignored Fields          |
+------------+-------------------------------+--------------------+------------------------------+
| Optimizer  | drug_type, prod_options,      |                    | desired_effects,             |
|            | depth                         |                    | initial_effects              |
+------------+-------------------------------+--------------------+------------------------------+
| Pathfinder | desired_effects               | initial_effects     | drug_type, prod_options,     |
|            |                               |                    | depth                        |
+------------+-------------------------------+--------------------+------------------------------+
```

**Note:**
- Use `prod_options` (like `strain`, `quality`, etc.) only for optimizer jobs where you want to maximize profit for a specific product.
- For pure pathfinding (effects mode), omit `prod_options`—just specify `depth`, `desired_effects`, and optionally `initial_effects`.

---

### List of All Valid Effects (Alphabetical)

```
Anti-gravity
Athletic
Balding
Bright-Eyed
Calming
Calorie-Dense
Cyclopean
Disorienting
Electrifying
Energizing
Euphoric
Foggy
Focused
Gingeritis
Glowing
Jennerising
Laxative
Long faced
Munchies
Paranoia
Refreshing
Schizophrenic
Sedating
Seizure-Inducing
Slippery
Smelly
Sneaky
Spicy
Thought-Provoking
Toxic
Tropic Thunder
Shrinking
Zombifying
```

*Use only these effects in your batch jobs!*

---

2. **Run the optimizer:**
   - From the project root:
     ```
     python -m src.cli.parallel_optimizer --jobs 4 --batch batch_jobs/batch_params.json
     ```
   - Results will be saved to `batch_jobs/parallel_optimizer_results.json` by default.
3. **Customize output location:**
   - Use `--results` to specify a custom results file location.

## Notes
- The core logic is in `src/parallel/batch_optimizer.py` for reuse in other interfaces.
- The CLI is a thin wrapper for the batch logic.
- Place all batch input/output files in `batch_jobs/` to keep your project organized.
