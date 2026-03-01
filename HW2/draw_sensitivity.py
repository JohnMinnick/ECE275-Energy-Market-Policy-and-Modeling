"""
Generate a sensitivity plot: Total cost vs. A-B flow limit.
Shows how congestion cost decreases as the limit increases, with the binding point marked.
"""

import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import os


def main():
    """Sweep the A-B flow limit from 0 to 120 MW and plot total cost."""

    # Problem data (same as solve.py)
    D_A, D_B, D_C = 200.0, 200.0, 200.0
    Cap_B, MC_B = 250.0, 22.0
    Cap_C, MC_C = 500.0, 26.0
    R_AB, R_BC, R_AC = 6.0, 6.0, 4.8

    c = np.array([MC_B, MC_C, 0, 0, 0, 0, 0, 0])
    A_eq = np.array([
        [0, 0, -1, 1, 0, 0, -1, 1],
        [1, 0,  1,-1,-1, 1,  0, 0],
        [0, 1,  0, 0, 1,-1,  1,-1],
        [0, 0, R_AB, -R_AB, R_BC, -R_BC, -R_AC, R_AC],
    ], dtype=float)
    b_eq = np.array([D_A, D_B, D_C, 0.0])
    big_M = 10000.0

    # Sweep flow limits
    limits = np.arange(0, 121, 1)
    costs = []

    for lim in limits:
        bounds = [
            (0, Cap_B), (0, Cap_C),
            (0, lim), (0, lim),       # A-B limited
            (0, big_M), (0, big_M),
            (0, big_M), (0, big_M),
        ]
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        costs.append(res.fun if res.success else np.nan)

    costs = np.array(costs)

    # Find where constraint stops binding (cost equals unconstrained)
    unconstrained_cost = costs[-1]
    binding_idx = np.where(np.abs(costs - unconstrained_cost) < 0.01)[0][0]
    binding_limit = limits[binding_idx]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(limits, costs, color='#2266aa', linewidth=2.5)
    ax.axhline(y=unconstrained_cost, color='#888888', linestyle='--',
               linewidth=1, label=f'Unconstrained cost (${unconstrained_cost:,.0f})')
    ax.axvline(x=binding_limit, color='#cc3333', linestyle='--',
               linewidth=1, label=f'Non-binding at {binding_limit} MW')

    # Mark the actual operating point (45 MW)
    cost_at_45 = costs[45]
    ax.plot(45, cost_at_45, 'o', color='#cc3333', markersize=10, zorder=5)
    ax.annotate(f'  Operating point\n  45 MW, ${cost_at_45:,.0f}',
                xy=(45, cost_at_45), fontsize=9,
                ha='left', va='bottom')

    # Mark binding point
    ax.plot(binding_limit, unconstrained_cost, 's', color='#22aa44', markersize=10, zorder=5)
    ax.annotate(f'  Non-binding\n  {binding_limit} MW',
                xy=(binding_limit, unconstrained_cost), fontsize=9,
                ha='left', va='top')

    # Shade the congestion cost region
    ax.fill_between([45, binding_limit],
                    [unconstrained_cost, unconstrained_cost],
                    [cost_at_45, unconstrained_cost],
                    alpha=0.15, color='#cc3333', label='Congestion cost region')

    ax.set_xlabel('A-B Flow Limit (MW)', fontsize=12)
    ax.set_ylabel('Total System Cost ($)', fontsize=12)
    ax.set_title('Total Cost vs. Transmission Constraint Level', fontsize=13)
    ax.legend(loc='upper right', fontsize=9)
    ax.set_xlim(0, 120)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    fig_path = os.path.join(script_dir, 'hw2_sensitivity.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {fig_path}")
    plt.show()


if __name__ == "__main__":
    main()
