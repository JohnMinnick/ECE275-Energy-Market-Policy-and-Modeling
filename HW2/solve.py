"""
ECE275 Homework 2: Linearized DC Load Flow

This script solves two problems:
1. Least-Cost Dispatch with Transmission Constraints (3-node DC load flow)
   - Parts a-d: LP formulation, LMPs, cost of congestion, congestion surplus
2. Power Transmission Distribution Factor (PTDF) Calculation

Network: 3-node triangle (A, B, C)
"""

import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt


# =============================================================================
# PROBLEM 1: Least-Cost Dispatch with DC Load Flow
# =============================================================================

def solve_dispatch():
    """
    Problem 1: Least-Cost Dispatch with DC Load Flow

    Network:    A --- B --- C (triangle)
    Demand:     200 MW at each node (A, B, C)
    Generation: Node B: 250 MW capacity @ $22/MWh
                Node C: 500 MW capacity @ $26/MWh
    Reactances: A-B = 6.0, B-C = 6.0, A-C = 4.8
    Constraint: |Flow on A-B| <= 45 MW (no other flow limits)

    LP Approach:
      Uses explicit flow variables with Kirchhoff's Current Law (KCL)
      at each node and Kirchhoff's Voltage Law (KVL) around the single
      independent loop (A->B->C->A).

    Decision Variables (10 total):
      g_B, g_C          = generation at nodes B and C (MW)
      t_AB, t_BA         = positive flow components on link A-B
      t_BC, t_CB         = positive flow components on link B-C
      t_AC, t_CA         = positive flow components on link A-C
      (Net flow from m->n = t_mn - t_nm)

    Objective: Minimize  22*g_B + 26*g_C
    """
    print("=" * 60)
    print("Problem 1: Least-Cost Dispatch with Transmission Constraints")
    print("=" * 60)

    # ==========================================
    # 1. PROBLEM DATA & CONSTANTS
    # ==========================================

    # Demand at each node (MW)
    D_A = 200.0
    D_B = 200.0
    D_C = 200.0

    # Generator capacities (MW) and marginal costs ($/MWh)
    Cap_B = 250.0
    MC_B = 22.0   # $/MWh

    Cap_C = 500.0
    MC_C = 26.0   # $/MWh

    # Line reactances (ohms)
    R_AB = 6.0
    R_BC = 6.0
    R_AC = 4.8

    # Flow limit on link A-B (MW, each direction)
    F_AB_max = 45.0

    # ==========================================
    # 2. OPTIMIZATION SETUP (LP)
    # ==========================================
    #
    # Decision variable vector x (10 variables):
    #   Index:  0     1     2      3      4      5      6      7
    #   Var:   g_B,  g_C,  t_AB,  t_BA,  t_BC,  t_CB,  t_AC,  t_CA
    #
    # Objective: minimize MC_B * g_B + MC_C * g_C
    #   (flow variables have zero cost)

    c = np.array([MC_B, MC_C, 0, 0, 0, 0, 0, 0])

    # --- EQUALITY CONSTRAINTS ---
    # KCL at each node: generation + imports - exports = demand
    #
    # Node A (no generator):
    #   (t_BA - t_AB) + (t_CA - t_AC) = D_A
    #   => 0*g_B + 0*g_C + (-1)*t_AB + (1)*t_BA + (0)*t_BC + (0)*t_CB + (-1)*t_AC + (1)*t_CA = 200
    #
    # Node B (generator g_B):
    #   g_B + (t_AB - t_BA) + (t_CB - t_BC) = D_B
    #   => 1*g_B + 0*g_C + (1)*t_AB + (-1)*t_BA + (-1)*t_BC + (1)*t_CB + (0)*t_AC + (0)*t_CA = 200
    #
    # Node C (generator g_C):
    #   g_C + (t_AC - t_CA) + (t_BC - t_CB) = D_C
    #   => 0*g_B + 1*g_C + (0)*t_AB + (0)*t_BA + (1)*t_BC + (-1)*t_CB + (1)*t_AC + (-1)*t_CA = 200
    #
    # KVL around loop A->B->C->A:
    #   R_AB*(t_AB - t_BA) + R_BC*(t_BC - t_CB) + R_CA*(t_CA - t_AC) = 0
    #   Note: going A->B->C->A, the last leg is C->A, so we use R_AC with sign for t_CA - t_AC
    #   R_AB*(t_AB - t_BA) + R_BC*(t_BC - t_CB) - R_AC*(t_AC - t_CA) = 0
    #   => 0 + 0 + R_AB*t_AB + (-R_AB)*t_BA + R_BC*t_BC + (-R_BC)*t_CB + (-R_AC)*t_AC + R_AC*t_CA = 0

    A_eq = np.array([
        # g_B, g_C, t_AB, t_BA, t_BC, t_CB, t_AC, t_CA
        [  0,   0,   -1,    1,    0,    0,   -1,    1],   # KCL Node A
        [  1,   0,    1,   -1,   -1,    1,    0,    0],   # KCL Node B
        [  0,   1,    0,    0,    1,   -1,    1,   -1],   # KCL Node C
        [  0,   0,  R_AB, -R_AB, R_BC, -R_BC, -R_AC, R_AC],  # KVL loop A->B->C->A
    ], dtype=float)

    b_eq = np.array([D_A, D_B, D_C, 0.0])

    # --- BOUNDS ---
    # Generators: 0 <= g_B <= 250, 0 <= g_C <= 500
    # Flow variables: all >= 0 (positive components)
    # t_AB, t_BA: 0 <= t <= 45 (A-B has flow limit)
    # t_BC, t_CB, t_AC, t_CA: 0 <= t <= big number (no limit)
    big_M = 10000.0  # Effectively unconstrained

    bounds = [
        (0, Cap_B),    # g_B
        (0, Cap_C),    # g_C
        (0, F_AB_max), # t_AB (limited)
        (0, F_AB_max), # t_BA (limited)
        (0, big_M),    # t_BC
        (0, big_M),    # t_CB
        (0, big_M),    # t_AC
        (0, big_M),    # t_CA
    ]

    # ==========================================
    # 3. SOLVE — CONSTRAINED CASE (45 MW limit on A-B)
    # ==========================================
    print("\n--- Part (a): Constrained Dispatch (A-B limit = 45 MW) ---")

    res_con = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if not res_con.success:
        print(f"ERROR: Constrained solve failed: {res_con.message}")
        return

    print_dispatch_results(res_con, "Constrained")

    # ==========================================
    # 4. SOLVE — UNCONSTRAINED CASE (relax A-B limit)
    # ==========================================
    print("\n--- Part (c): Unconstrained Dispatch (no flow limits) ---")

    bounds_uncon = [
        (0, Cap_B),  # g_B
        (0, Cap_C),  # g_C
        (0, big_M),  # t_AB (relaxed)
        (0, big_M),  # t_BA (relaxed)
        (0, big_M),  # t_BC
        (0, big_M),  # t_CB
        (0, big_M),  # t_AC
        (0, big_M),  # t_CA
    ]

    res_uncon = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds_uncon, method='highs')

    if not res_uncon.success:
        print(f"ERROR: Unconstrained solve failed: {res_uncon.message}")
        return

    print_dispatch_results(res_uncon, "Unconstrained")

    # ==========================================
    # 5. LMPs (Part b) — from dual variables on KCL constraints
    # ==========================================
    print("\n--- Part (b): Locational Marginal Prices (LMPs) ---")

    # The dual variables on the KCL (power balance) constraints
    # give the marginal cost of serving 1 more MW at each node
    duals = res_con.eqlin.marginals
    LMP_A = duals[0]  # Dual on KCL Node A
    LMP_B = duals[1]  # Dual on KCL Node B
    LMP_C = duals[2]  # Dual on KCL Node C

    print(f"  LMP at Node A: ${LMP_A:.2f}/MWh")
    print(f"  LMP at Node B: ${LMP_B:.2f}/MWh")
    print(f"  LMP at Node C: ${LMP_C:.2f}/MWh")
    print(f"  KVL dual:      ${duals[3]:.4f}")

    # Verify by incrementing load by 1 MW at each node
    print("\n  Verification (increment load by 1 MW at each node):")
    for node_idx, node_name in enumerate(["A", "B", "C"]):
        b_eq_inc = b_eq.copy()
        b_eq_inc[node_idx] += 1.0
        res_inc = linprog(c, A_eq=A_eq, b_eq=b_eq_inc, bounds=bounds, method='highs')
        if res_inc.success:
            marginal = res_inc.fun - res_con.fun
            print(f"    Node {node_name}: Delta Cost = ${marginal:.2f}/MWh (vs LMP = ${duals[node_idx]:.2f})")

    # ==========================================
    # 6. COST OF CONGESTION (Part c)
    # ==========================================
    print("\n--- Part (c): Cost of Congestion ---")

    cost_congested = res_con.fun
    cost_uncongested = res_uncon.fun
    congestion_cost = cost_congested - cost_uncongested

    print(f"  Constrained total cost:   ${cost_congested:,.2f}")
    print(f"  Unconstrained total cost: ${cost_uncongested:,.2f}")
    print(f"  Cost of congestion:       ${congestion_cost:,.2f}")

    # Find the binding transmission limit
    print("\n  Searching for binding constraint level...")
    for limit in np.arange(0, 200, 1):
        bounds_test = list(bounds_uncon)
        bounds_test[2] = (0, limit)  # t_AB limit
        bounds_test[3] = (0, limit)  # t_BA limit
        res_test = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds_test, method='highs')
        if res_test.success and abs(res_test.fun - cost_uncongested) < 0.01:
            print(f"  Constraint becomes non-binding at A-B limit = {limit:.0f} MW")
            break

    # ==========================================
    # 7. CONGESTION SURPLUS (Part d)
    # ==========================================
    print("\n--- Part (d): Congestion Surplus ---")

    # Consumer payments: each node pays LMP * demand
    consumer_payment = LMP_A * D_A + LMP_B * D_B + LMP_C * D_C
    print(f"  Consumer payments: {LMP_A:.2f}*{D_A:.0f} + {LMP_B:.2f}*{D_B:.0f} + {LMP_C:.2f}*{D_C:.0f}")
    print(f"                   = ${consumer_payment:,.2f}")

    # Generator revenue: each generator receives LMP at its node * generation
    x = res_con.x
    g_B, g_C = x[0], x[1]
    generator_revenue = LMP_B * g_B + LMP_C * g_C
    print(f"  Generator revenue: {LMP_B:.2f}*{g_B:.1f} + {LMP_C:.2f}*{g_C:.1f}")
    print(f"                   = ${generator_revenue:,.2f}")

    # Congestion surplus = consumer payments - generator revenue
    congestion_surplus = consumer_payment - generator_revenue
    print(f"  Congestion surplus (ISO net revenue): ${congestion_surplus:,.2f}")
    print(f"  Cost of congestion (Part c):          ${congestion_cost:,.2f}")
    print(f"  Are they equal? {'Yes' if abs(congestion_surplus - congestion_cost) < 0.01 else 'No'}")

    # ==========================================
    # 8. VISUALIZATION
    # ==========================================
    plot_dispatch(res_con, res_uncon, LMP_A, LMP_B, LMP_C)

    return res_con, res_uncon


def print_dispatch_results(res, label):
    """
    Print the dispatch results from a linprog solution.

    Args:
        res:   scipy.optimize.OptimizeResult from linprog
        label: string label for the scenario (e.g., "Constrained")
    """
    x = res.x
    g_B, g_C = x[0], x[1]
    t_AB, t_BA = x[2], x[3]
    t_BC, t_CB = x[4], x[5]
    t_AC, t_CA = x[6], x[7]

    print(f"  Total Cost: ${res.fun:,.2f}")
    print(f"  Generation:  B = {g_B:.1f} MW,  C = {g_C:.1f} MW,  Total = {g_B + g_C:.1f} MW")
    print(f"  Net Flows:")
    print(f"    A->B: {t_AB - t_BA:+.1f} MW  (t_AB={t_AB:.1f}, t_BA={t_BA:.1f})")
    print(f"    B->C: {t_BC - t_CB:+.1f} MW  (t_BC={t_BC:.1f}, t_CB={t_CB:.1f})")
    print(f"    A->C: {t_AC - t_CA:+.1f} MW  (t_AC={t_AC:.1f}, t_CA={t_CA:.1f})")


def plot_dispatch(res_con, res_uncon, LMP_A, LMP_B, LMP_C):
    """
    Plot dispatch comparison and LMPs for constrained vs unconstrained cases.

    Args:
        res_con:   Constrained dispatch result
        res_uncon: Unconstrained dispatch result
        LMP_A, LMP_B, LMP_C: Locational marginal prices at each node
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- Left: Generation Dispatch Comparison ---
    ax1 = axes[0]
    x_con = res_con.x
    x_uncon = res_uncon.x

    categories = ['Constrained\n(45 MW limit)', 'Unconstrained']
    gen_B = [x_con[0], x_uncon[0]]
    gen_C = [x_con[1], x_uncon[1]]

    bar_width = 0.35
    x_pos = np.arange(len(categories))

    ax1.bar(x_pos, gen_B, bar_width, color='#66b3ff', label='Gen B ($22/MWh)')
    ax1.bar(x_pos, gen_C, bar_width, bottom=gen_B, color='#ff9999', label='Gen C ($26/MWh)')
    ax1.axhline(y=600, color='gray', linestyle='--', alpha=0.5, label='Total Demand (600 MW)')
    ax1.set_ylabel('Generation (MW)')
    ax1.set_title('Dispatch Comparison')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(categories)
    ax1.legend()
    ax1.set_ylim(0, 700)

    # --- Right: LMPs ---
    ax2 = axes[1]
    nodes = ['Node A', 'Node B', 'Node C']
    lmps = [LMP_A, LMP_B, LMP_C]
    colors = ['#ffcc99', '#66b3ff', '#ff9999']

    bars = ax2.bar(nodes, lmps, color=colors, edgecolor='black', linewidth=0.8)
    ax2.set_ylabel('LMP ($/MWh)')
    ax2.set_title('Locational Marginal Prices (Constrained)')

    # Add value labels on bars
    for bar, val in zip(bars, lmps):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f'${val:.2f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    # Save figure in the same directory as this script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fig_path = os.path.join(script_dir, 'hw2_dispatch.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"\n  Figure saved: {fig_path}")
    plt.show()


# =============================================================================
# PROBLEM 2: PTDF Calculation
# =============================================================================

def solve_ptdf():
    """
    Problem 2: PTDF Calculation

    Network:    A --- B --- C (triangle)
    Reactances: A-B = 1.7, B-C = 1.7, A-C = 1.4
    Hub node:   A (reference / swing bus)

    PTDFs are calculated by:
      1. Build the nodal susceptance matrix B (using b = 1/R for each line)
      2. Remove the hub node (A) row and column to get B_reduced
      3. Invert B_reduced to get X = B_reduced^{-1}
      4. For injection at node m, withdrawal at hub:
         PTDF_{m, j->k} = b_jk * (X_{m,j} - X_{m,k})
         where indices are relative to the reduced matrix (without hub)
         and X_{hub,*} = 0 by convention.
    """
    print("\n" + "=" * 60)
    print("Problem 2: Power Transmission Distribution Factors (PTDFs)")
    print("=" * 60)

    # ==========================================
    # 1. PROBLEM DATA & CONSTANTS
    # ==========================================

    # Node ordering: A=0, B=1, C=2
    # Hub node: A (index 0)

    # Line reactances
    R_AB = 1.7
    R_BC = 1.7
    R_AC = 1.4

    # Susceptances (b = 1/R)
    b_AB = 1.0 / R_AB
    b_BC = 1.0 / R_BC
    b_AC = 1.0 / R_AC

    print(f"\n  Susceptances:")
    print(f"    b_AB = 1/{R_AB} = {b_AB:.6f}")
    print(f"    b_BC = 1/{R_BC} = {b_BC:.6f}")
    print(f"    b_AC = 1/{R_AC} = {b_AC:.6f}")

    # ==========================================
    # 2. BUILD THE NODAL SUSCEPTANCE MATRIX (B)
    # ==========================================
    # Full B matrix (3x3) for nodes A, B, C:
    #   B[i,i] = sum of susceptances of lines connected to node i
    #   B[i,j] = -susceptance of line between i and j

    B_full = np.array([
        [ b_AB + b_AC,   -b_AB,        -b_AC       ],   # Node A
        [-b_AB,           b_AB + b_BC,  -b_BC       ],   # Node B
        [-b_AC,          -b_BC,          b_BC + b_AC ],   # Node C
    ])

    print(f"\n  Full B matrix (3x3):")
    print(f"    {B_full}")

    # ==========================================
    # 3. REDUCE MATRIX (remove hub node A = row 0, col 0)
    # ==========================================
    # Remaining nodes: B (index 0 in reduced), C (index 1 in reduced)

    B_red = B_full[1:, 1:]  # Remove row 0 and col 0

    print(f"\n  Reduced B matrix (hub A removed):")
    print(f"    {B_red}")

    # ==========================================
    # 4. INVERT TO GET X MATRIX
    # ==========================================

    X = np.linalg.inv(B_red)

    print(f"\n  X = B_reduced^(-1):")
    print(f"    {X}")

    # X is indexed by reduced node indices:
    #   X[0,0] = X_BB, X[0,1] = X_BC
    #   X[1,0] = X_CB, X[1,1] = X_CC
    # For hub node A: X_A* = 0 by convention

    # ==========================================
    # 5. CALCULATE PTDFs
    # ==========================================
    # PTDF_{m, j->k} = b_jk * (X_mj - X_mk)
    # where X values use the reduced matrix, with X_A* = 0
    #
    # Reduced indices: B=0, C=1 in X matrix; A values are 0

    print(f"\n  --- PTDF Calculations ---")
    print(f"  Formula: PTDF_{{m, j->k}} = b_{{jk}} * (X_mj - X_mk)")
    print(f"  (Hub node A has X_A* = 0)\n")

    # Helper: get X value for a node pair in the reduced matrix
    # node_map: A->None (hub, value=0), B->0, C->1
    def get_X(m, n):
        """
        Get X[m,n] from the reduced X matrix.
        m, n are node names: 'A', 'B', or 'C'.
        Returns 0 if either is the hub node (A).
        """
        node_idx = {'B': 0, 'C': 1}
        if m == 'A' or n == 'A':
            return 0.0
        return X[node_idx[m], node_idx[n]]

    # Line susceptance lookup
    line_b = {
        ('A', 'B'): b_AB, ('B', 'A'): b_AB,
        ('B', 'C'): b_BC, ('C', 'B'): b_BC,
        ('A', 'C'): b_AC, ('C', 'A'): b_AC,
    }

    def calc_ptdf(m, j, k):
        """
        Calculate PTDF for injection at node m, flow on line j->k.
        PTDF_{m, j->k} = b_jk * (X_mj - X_mk)

        Args:
            m: injection node name ('A', 'B', or 'C')
            j: line start node
            k: line end node
        Returns:
            PTDF value
        """
        b_jk = line_b[(j, k)]
        X_mj = get_X(m, j)
        X_mk = get_X(m, k)
        ptdf = b_jk * (X_mj - X_mk)
        print(f"  PTDF_{{{m},{j}{k}}} = b_{{{j}{k}}} * (X_{{{m}{j}}} - X_{{{m}{k}}})")
        print(f"          = {b_jk:.6f} * ({X_mj:.6f} - {X_mk:.6f})")
        print(f"          = {ptdf:.6f}\n")
        return ptdf

    # Calculate all requested PTDFs
    results = {}
    results['C,AB'] = calc_ptdf('C', 'A', 'B')
    results['C,BA'] = calc_ptdf('C', 'B', 'A')
    results['C,AC'] = calc_ptdf('C', 'A', 'C')
    results['C,BC'] = calc_ptdf('C', 'B', 'C')
    results['B,AC'] = calc_ptdf('B', 'A', 'C')
    results['A,AC'] = calc_ptdf('A', 'A', 'C')

    # ==========================================
    # 6. SUMMARY TABLE
    # ==========================================
    print("  --- Summary ---")
    print(f"  {'PTDF':>12}  {'Value':>10}")
    print(f"  {'-'*12}  {'-'*10}")
    for key, val in results.items():
        print(f"  PTDF_{{{key}:>4}}  {val:>10.6f}")

    # Verification: PTDF_{C,AB} = -PTDF_{C,BA} (opposite direction on same line)
    print(f"\n  Verification:")
    print(f"    PTDF_{{C,AB}} = {results['C,AB']:.6f}")
    print(f"    PTDF_{{C,BA}} = {results['C,BA']:.6f}")
    print(f"    Sum = {results['C,AB'] + results['C,BA']:.6f} (should be 0)")

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point for the homework solution."""
    print("--- ECE275 Homework 2: Linearized DC Load Flow ---\n")

    # Solve Problem 1: Dispatch with transmission constraints
    dispatch_results = solve_dispatch()

    # Solve Problem 2: PTDF calculations
    ptdf_results = solve_ptdf()


if __name__ == "__main__":
    main()
