---
description: Scaffold a new homework folder with LaTeX and Python templates
---

# New Homework Setup

Creates a new `HWn/` folder with a LaTeX report template and a Python solution script.

## Steps

1. Determine the homework number. If not specified, look at existing `HW*` folders and use the next number.

2. Create the homework directory:
```powershell
mkdir c:\AGCoding\ECE275-Energy-Market-Policy-and-Modeling\HWn
```

3. Create `main.tex` from the LaTeX report skill template. Read the template at:
   `.agent/skills/latex-report/template.tex`
   
   Update the following fields in the template:
   - `\title{ECE275: Homework \#N}` — set the correct homework number
   - The date in the `\author` block — set to the current month and year
   
   Save to `HWn/main.tex`.

4. Create `solve.py` with the following boilerplate:

```python
"""
ECE275 Homework N: [Problem Title]

This script solves the optimization / modeling problem for HW N.
"""

import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Main entry point for the homework solution."""
    print("--- ECE275 Homework N ---\n")
    
    # ==========================================
    # 1. PROBLEM DATA & CONSTANTS
    # ==========================================
    # TODO: Define problem parameters here
    
    # ==========================================
    # 2. OPTIMIZATION SETUP
    # ==========================================
    # TODO: Formulate the optimization problem
    
    # ==========================================
    # 3. SOLVE
    # ==========================================
    # TODO: Call the solver
    
    # ==========================================
    # 4. RESULTS ANALYSIS
    # ==========================================
    # TODO: Interpret and print results
    
    # ==========================================
    # 5. VISUALIZATION
    # ==========================================
    # TODO: Plot results and save figures
    

if __name__ == "__main__":
    main()
```

   Update the homework number in the docstring and print statement. Save to `HWn/solve.py`.

5. Report to the user that the new homework folder is ready with both template files.

## Notes
- If the instructor provides a PDF assignment, the user should place it in the `HWn/` folder manually.
- The LaTeX template includes all standard packages and the code listing style from HW1.
