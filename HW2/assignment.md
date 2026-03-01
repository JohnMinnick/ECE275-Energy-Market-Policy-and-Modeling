# HW2: Linearized DC Load Flow — ECE275 (Due 3/3/2026)

## Background Notes

Kirchhoff's laws (as approximated by a DC load flow) imply that:

- **Current Law Analog**: Net power inflow into a node = 0 (demand = supply + net transmission flows in)
- **Voltage Law Analog**: The sum of the products of power flow and reactance around a loop in a network = 0

These laws uniquely define a set of transmission flows on the network, given the net injections (supply - demand) at each node.

### Notation

| Symbol | Meaning |
|---|---|
| y_im | Generation by the i-th plant at node m |
| LOAD_m | Quantity demanded at node m |
| t_mn | Positive component of MW flow on link m->n. Net flow = t_mn - t_nm |
| T_mn | MW capacity of link m->n |
| R_mn | Effective reactance (ohms) between nodes m and n |
| N(m) | Set of nodes directly connected to node m |
| MN(v) | Ordered set of links on voltage loop v |
| V | Set of independent voltage loops |

### Kirchhoff's Current Law (KCL) for node m

```
sum_i(y_im) + sum_{n in N(m)}(t_nm - t_mn) = LOAD_m
```

(generation + imports - exports = load)

### Kirchhoff's Voltage Law (KVL)

```
sum_{mn in MN(v)} R_mn * (t_mn - t_nm) = 0   for each voltage loop v
```

### PTDFs

A 1 MW injection at node m and a matching 1 MW withdrawal at a predefined "hub" node results in a net flow of PTDF_{m,jk} on a transmission line from node j to node k. Doubling the injection doubles the flow.

---

## Problem 1: Least-Cost Dispatch

**Network**: 3 nodes (A, B, C) in a triangle configuration, with transmission lines linking each pair.

**Demand**: 200 MW at each node.

**Generation**:
- Node C: 500 MW capacity, Marginal Cost = $26/MWh
- Node B: 250 MW capacity, Marginal Cost = $22/MWh

**Reactances**:
- A-B: R = 6.0
- B-C: R = 6.0
- A-C: R = 4.8

**Constraints**: Link A-B has a flow limit of 45 MW in each direction. No other flow limits.

### Part (a)
Set up and solve a linear optimization program to determine the least cost dispatch, subject to capacity limits and transmission constraints. Use 2 or 3 KCL equations and 1 KVL equation with explicit flow variables. Compare to PTDF formulation.

### Part (b)
What is the marginal cost of meeting demand at each node? (Look at dual variables for the KCL constraints.) Explain each in terms of how generation at C and B changes if you increase load at each node by 1 MW. Is there anything odd about A's price? (Is it higher or lower than both B and C? How can that be?)

### Part (c)
What is the "cost of congestion"? (How much money would be saved with no transmission constraints?) At what level of the transmission constraint does it become binding?

### Part (d)
Calculate the "congestion surplus" (ISO net revenue):
- Consumer payments = sum of (LMP_node * demand_node)
- Generator revenue = sum of (LMP_node * generation_node)
- Congestion surplus = Consumer payments - Generator revenue

Example: 2-node system, 100 MW consumption, LMP_D=$25, LMP_E=$40:
- Consumer pays: 100 * $40 = $4000
- Generator receives: 100 * $25 = $2500
- Congestion surplus = $4000 - $2500 = $1500

Is the congestion surplus the same as the "cost of congestion" from part (c)?

---

## Problem 2: PTDF Calculation

**Network**: Same 3-node triangle (A, B, C).

**Reactances** (different from Problem 1):
- A-B: R = 1.7
- B-C: R = 1.7
- A-C: R = 1.4

**Hub node**: A

Consider a 1 MW injection at m=C, and 1 MW matching withdrawal at hub A.

Calculate the following PTDFs:
- PTDF_{C,AB}
- PTDF_{C,BA}
- PTDF_{C,AC}
- PTDF_{C,BC}
- PTDF_{B,AC}
- PTDF_{A,AC}
