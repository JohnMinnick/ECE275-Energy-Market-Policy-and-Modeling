---
description: Run a homework Python script in the virtual environment
---

# Run Python Script

Runs a Python solution script from a homework folder using the project's virtual environment.

## Steps

1. Identify which homework and script to run. Default is `HWx/solve.py`. If not specified, ask the user.

// turbo
2. Run the script using the venv Python:
```powershell
c:\AGCoding\ECE275-Energy-Market-Policy-and-Modeling\.venv\Scripts\python.exe solve.py
```
Working directory: `c:\AGCoding\ECE275-Energy-Market-Policy-and-Modeling\HWx\`

3. Report the output to the user. If there are errors:
   - Read the traceback carefully
   - Fix the script
   - Re-run from step 2

4. If the script generates figures (`.png` files), confirm they were saved and are ready for LaTeX inclusion.

## Notes
- Always use the venv Python (`.venv\Scripts\python.exe`) to ensure the correct packages are available.
- If a new package is needed, install it with `.venv\Scripts\pip.exe install <package>` and add it to `requirements.txt`.
- For interactive exploration, use `.venv\Scripts\jupyter.exe notebook` from the homework directory.
