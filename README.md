# ECE 275: Electricity Market, Policy, and Modeling

**University of California, Santa Cruz — Winter 2026**
**Department of Electrical and Computer Engineering**

## Overview

This repository contains homework assignments for ECE 275. Each homework combines:
- **Python** scripts for numerical analysis, optimization, and visualization
- **LaTeX** reports (IEEEtran format) documenting solutions and analysis

## Repository Structure

```
ECE275-Energy-Market-Policy-and-Modeling/
├── HW1/                    # Homework 1
│   ├── main.tex            # LaTeX report source
│   ├── solve.py            # Python solution script
│   └── *.png               # Generated figures
├── HW2/                    # Homework 2
│   └── ...
├── .agent/                 # Agent rules, workflows, and skills
│   ├── rules.md
│   ├── workflows/
│   └── skills/
├── .venv/                  # Python virtual environment (gitignored)
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md               # This file
```

## Setup

### Prerequisites
- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **MiKTeX** (Windows) — [miktex.org](https://miktex.org/download)

### Install Python Dependencies

```bash
# Create virtual environment (first time only)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Compile a LaTeX Report

```bash
cd HW1
pdflatex main.tex
pdflatex main.tex   # Run twice for cross-references
```

## Workflows

| Workflow | Description |
|---|---|
| `/compile-latex` | Compile a homework LaTeX report to PDF |
| `/new-hw` | Scaffold a new homework folder with templates |
| `/run-python` | Run a homework Python script in the venv |

## Author

**John R. Minnick** — UC Santa Cruz, ECE

> **Disclaimer:** Generative AI was used for the creation of document structure and some code implementation. All written content and opinions are solely those of the author.
