---
description: Compile a LaTeX homework report to PDF
---

# Compile LaTeX Report

Compiles a homework's `main.tex` into a PDF using `pdflatex`.

## Steps

1. Identify which homework to compile (e.g., `HW1`, `HW2`, etc.). If not specified, ask the user.

// turbo
2. Run `pdflatex` from the homework directory (first pass):
```powershell
pdflatex -interaction=nonstopmode main.tex
```
Working directory: `c:\AGCoding\ECE275-Energy-Market-Policy-and-Modeling\HWx\`

// turbo
3. Run `pdflatex` a second time (resolves cross-references, table of contents, etc.):
```powershell
pdflatex -interaction=nonstopmode main.tex
```
Working directory: `c:\AGCoding\ECE275-Energy-Market-Policy-and-Modeling\HWx\`

4. Check the output for errors. If there are LaTeX errors:
   - Read the `.log` file for details
   - Fix the issues in `main.tex`
   - Re-run from step 2

5. Confirm `main.pdf` was generated successfully. Report the file path to the user.

## Notes
- MiKTeX will auto-install missing LaTeX packages on first use (may prompt).
- If BibTeX is needed, run `bibtex main` between the two `pdflatex` runs.
- The `.gitignore` excludes all LaTeX build artifacts (`.aux`, `.log`, `.pdf`, etc.).
