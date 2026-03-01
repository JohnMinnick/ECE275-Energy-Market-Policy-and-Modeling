---
name: Energy Modeling
description: How to write Python scripts for energy market optimization and modeling problems
---

# Energy Modeling Skill

This skill covers writing Python scripts for ECE 275 energy market optimization problems.

## Script Structure

Every homework Python script should follow this 5-section pattern:

```python
"""
ECE275 Homework N: [Problem Title]

Brief description of what the script solves.
"""

import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Main entry point."""
    
    # ==========================================
    # 1. PROBLEM DATA & CONSTANTS
    # ==========================================
    # Define all given parameters here
    
    # ==========================================
    # 2. OPTIMIZATION SETUP
    # ==========================================
    # Define decision variables, objective, constraints
    
    # ==========================================
    # 3. SOLVE
    # ==========================================
    # Call the solver and check for success
    
    # ==========================================
    # 4. RESULTS ANALYSIS
    # ==========================================
    # Interpret primal and dual solutions
    
    # ==========================================
    # 5. VISUALIZATION
    # ==========================================
    # Plot results and save figures


if __name__ == "__main__":
    main()
```

## Linear Programming with scipy

Use `scipy.optimize.linprog` for straightforward LP problems:

```python
from scipy.optimize import linprog

# Objective: minimize c^T x
c = np.array([cost1 * duration1, cost2 * duration2, ...])

# Equality constraints: A_eq @ x = b_eq
A_eq = [[1, 1, 0, 0], [0, 0, 1, 1]]
b_eq = [demand1, demand2]

# Inequality constraints: A_ub @ x <= b_ub
A_ub = [[0, 0, T1, T2]]
b_ub = [energy_limit]

# Bounds: 0 <= x_i <= capacity_i
bounds = [(0, cap1), (0, cap2), ...]

# Solve
result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub,
                 bounds=bounds, method='highs')
```

## Linear Programming with PuLP

Use `pulp` for more complex or readable formulations:

```python
import pulp

# Create problem
prob = pulp.LpProblem("Dispatch", pulp.LpMinimize)

# Decision variables
gen = pulp.LpVariable.dicts("Gen", plants, lowBound=0)

# Objective
prob += pulp.lpSum(cost[p] * gen[p] for p in plants)

# Constraints
prob += pulp.lpSum(gen[p] for p in plants) == demand

# Solve
prob.solve(pulp.PULP_CBC_CMD(msg=0))
```

## Interpreting Dual Variables

Dual variables (shadow prices / marginal costs) are key economic indicators:

```python
# scipy: duals are attached to the result
duals_eq = result.eqlin.marginals    # Equality constraint duals
duals_ub = result.ineqlin.marginals  # Inequality constraint duals

# UNIT CONVERSION: scipy duals are in $/unit-of-constraint per unit-of-variable
# If objective is in $ and constraint is in MW, dual is in $/MW for the full period.
# Divide by hours to get $/MWh:
marginal_cost = duals_eq[period_idx] / hours_in_period
```

## Plotting Conventions

### Stacked Bar Charts (Dispatch)

```python
fig, ax = plt.subplots(figsize=(10, 6))

# Stack from cheapest to most expensive
ax.bar(periods, hydro, color='#99ff99', label='Hydro ($0)')
ax.bar(periods, oil, bottom=hydro, color='#ff9999', label='Oil ($90)')
ax.bar(periods, diesel, bottom=np.add(hydro, oil), color='#66b3ff', label='Diesel ($130)')

ax.set_ylabel("Generation (MW)")
ax.set_title("Optimal Dispatch")
ax.legend()
plt.tight_layout()
plt.savefig("dispatch.png", dpi=150, bbox_inches='tight')
plt.show()
```

### Key Plotting Tips

- Always save figures as PNG with `dpi=150` and `bbox_inches='tight'`
- Use descriptive filenames (e.g., `dispatch_comparison.png`, `cost_curve.png`)
- Stack bars from cheapest to most expensive (merit order)
- Use consistent color schemes across subplots
- Add clear titles, axis labels, and legends

## Common Energy Market Concepts

| Concept | Description |
|---|---|
| **Merit Order** | Dispatch generators cheapest-first |
| **Marginal Cost** | Cost of producing one more MWh (set by the most expensive active generator) |
| **Shadow Price** | Value of relaxing a constraint by one unit |
| **Capacity Factor** | Actual generation / maximum possible generation |
| **Load Duration Curve** | Demand sorted from highest to lowest |
| **Economic Dispatch** | Minimize total cost while meeting demand |
