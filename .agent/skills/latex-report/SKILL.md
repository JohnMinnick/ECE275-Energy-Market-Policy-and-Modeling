---
name: LaTeX Report
description: How to write ECE 275 LaTeX homework reports using the IEEEtran template
---

# LaTeX Report Skill

This skill covers writing homework reports for ECE 275 using the IEEEtran document class.

## Template

A ready-to-use template is available at:
`.agent/skills/latex-report/template.tex`

Copy this template into a new `HWn/main.tex` and update:
- The homework number in `\title{}`
- The date in `\author{}`
- The section content

## Document Structure

Every homework report should follow this structure:

```
\section{Problem Title}
  \subsection{Part A: ...}
    - Problem statement (italicized prompt)
    - Analysis text
    - Tables with colored cells (if applicable)
    - Figures (if applicable)
  \subsection{Part B: ...}
    ...

\section{Appendix: Python Code}
  - Full code listing using lstlisting environment
```

## Standard Packages

Always include these in the preamble (already in the template):

| Package | Purpose |
|---|---|
| `amsmath, amssymb` | Math symbols and environments |
| `graphicx` | Figure inclusion (`\includegraphics`) |
| `listings` | Code listings with syntax highlighting |
| `booktabs` | Professional-quality tables (`\toprule`, `\midrule`, `\bottomrule`) |
| `multirow` | Multi-row table cells |
| `geometry` | Page margin control |
| `xcolor` + `[table]` | Cell coloring with `\cellcolor{}` |
| `placeins` | `\FloatBarrier` to control float placement |

## Table Coloring Convention

Use these predefined pastel colors for policy evaluation tables:

```latex
\definecolor{mygreen}{rgb}{0.7, 1, 0.7}   % High suitability
\definecolor{myyellow}{rgb}{1, 1, 0.7}     % Medium suitability
\definecolor{myred}{rgb}{1, 0.7, 0.7}      % Low / negative suitability
```

Apply with: `\cellcolor{mygreen} Cell text`

## Code Listings

Use the `mystyle` listing style for all Python code:

```latex
\begin{lstlisting}[language=Python, caption=Description of the code]
import numpy as np
# ... your code ...
\end{lstlisting}
```

The `mystyle` is defined in the template with:
- Light background, green comments, magenta keywords, purple strings
- Line numbers on the left
- Word wrapping enabled

## Figures

Save Python-generated figures as PNG and include them:

```latex
\FloatBarrier
\begin{figure}[h]
    \centering
    \includegraphics[width=0.6\textwidth]{filename.png}
    \caption{Descriptive caption explaining what the figure shows.}
    \label{fig:descriptive_label}
\end{figure}
\FloatBarrier
```

## Tips

- Use `\FloatBarrier` (from `placeins`) before and after figures/tables to keep them near the relevant text.
- Use `\\` and `\par` for paragraph breaks in analysis sections.
- Always include the AI disclaimer `\thanks{}` block in the author field.
- Compile twice with `pdflatex` to resolve cross-references.
