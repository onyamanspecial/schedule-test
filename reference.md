# Cost Calculation Documentation for Scheduled I Effect Optimizer

This document outlines the cost calculation methods for producing marijuana, meth, and cocaine in the `Scheduled_I_Effect_Optimizer.py` file.

## 1. Marijuana Cost Calculation

The cost for marijuana is calculated in the `calculate_production_cost` function as follows:

```python
def calculate_production_cost(drug_type, subtype, units_per_seed=None):
    if drug_type == 'Marijuana':
        strain, seed_cost = subtype
        soil_per_seed = PLANT_SOIL_COST / PLANT_SOIL_USES
        total_per_seed = seed_cost + soil_per_seed
        return total_per_seed / units_per_seed, strain
```

### Parameters:
- `strain`: The selected strain of marijuana.
- `seed_cost`: The cost of the selected strain.
- `units_per_seed`: The number of units produced per seed.

### Constants:
- `PLANT_SOIL_COST`: 60 (total cost for soil).
- `PLANT_SOIL_USES`: 3 (number of uses for the soil).

### Calculation:
- Cost of soil per seed:
  \[
  \text{soil\_per\_seed} = \frac{\text{PLANT\_SOIL\_COST}}{\text{PLANT\_SOIL\_USES}} = \frac{60}{3} = 20
  \]
- Total cost per seed:
  \[
  \text{total\_per\_seed} = \text{seed\_cost} + \text{soil\_per\_seed}
  \]
- Production cost per unit:
  \[
  \text{production\_cost} = \frac{\text{total\_per\_seed}}{\text{units\_per\_seed}}
  \]

## 2. Meth Cost Calculation

The cost for meth is calculated similarly:

```python
elif drug_type == 'Meth':
    quality, pseudo_cost = subtype
    total_batch_cost = pseudo_cost + METH_ACID_COST + METH_PHOSPHORUS_COST
    return total_batch_cost / METH_BATCH_SIZE, quality
```

### Parameters:
- `quality`: The selected quality of meth.
- `pseudo_cost`: The cost associated with the selected quality.

### Constants:
- `METH_ACID_COST`: 40 (cost of acid used in production).
- `METH_PHOSPHORUS_COST`: 40 (cost of phosphorus used in production).
- `METH_BATCH_SIZE`: 10 (number of units produced in a batch).

### Calculation:
- Total batch cost:
  \[
  \text{total\_batch\_cost} = \text{pseudo\_cost} + \text{METH\_ACID\_COST} + \text{METH\_PHOSPHORUS\_COST}
  \]
- Production cost per unit:
  \[
  \text{production\_cost} = \frac{\text{total\_batch\_cost}}{\text{METH\_BATCH\_SIZE}}
  \]

## 3. Cocaine Cost Calculation

The cost for cocaine is calculated as follows:

```python
elif drug_type == 'Cocaine':
    soil_per_seed = PLANT_SOIL_COST / PLANT_SOIL_USES
    seed_cost = 150
    gasoline_cost = INGREDIENT_PRICES['Gasoline'] * GASOLINE_PER_COCAINE_UNIT
    total_per_seed = seed_cost + soil_per_seed
    return (total_per_seed / units_per_seed) + gasoline_cost, 'Cocaine Seed'
```

### Constants:
- `PLANT_SOIL_COST`: 60 (total cost for soil).
- `PLANT_SOIL_USES`: 3 (number of uses for the soil).
- `seed_cost`: 150 (cost of the cocaine seed).
- `GASOLINE_PER_COCAINE_UNIT`: \( \frac{1}{20} \) (amount of gasoline used per unit of cocaine).
- `INGREDIENT_PRICES['Gasoline']`: 5 (cost of gasoline).

### Calculation:
- Cost of soil per seed:
  \[
  \text{soil\_per\_seed} = \frac{\text{PLANT\_SOIL\_COST}}{\text{PLANT\_SOIL\_USES}} = \frac{60}{3} = 20
  \]
- Total cost per seed:
  \[
  \text{total\_per\_seed} = \text{seed\_cost} + \text{soil\_per\_seed} = 150 + 20 = 170
  \]
- Production cost per unit:
  \[
  \text{production\_cost} = \frac{\text{total\_per\_seed}}{\text{units\_per\_seed}} + \text{gasoline\_cost}
  \]
- Gasoline cost:
  \[
  \text{gasoline\_cost} = \text{INGREDIENT\_PRICES['Gasoline']} \times \text{GASOLINE\_PER\_COCAINE\_UNIT} = 5 \times \frac{1}{20} = 0.25
  \]

## Summary of Costs
- **Marijuana**: 
  - Cost per unit = \(\frac{\text{seed\_cost} + 20}{\text{units\_per\_seed}}\)
- **Meth**: 
  - Cost per unit = \(\frac{\text{pseudo\_cost} + 40 + 40}{10}\)
- **Cocaine**: 
  - Cost per unit = \(\frac{170}{\text{units\_per\_seed}} + 0.25\)

These calculations ensure that the production costs reflect the various inputs and overheads associated with each drug type.