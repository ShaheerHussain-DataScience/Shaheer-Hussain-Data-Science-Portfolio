#!/usr/bin/env python3
"""
Prescriptive analytics with LP: optimal restaurant staffing from Seaborn 'tips'.

- Decision: number of servers per shift (day x time)
- Objective: minimize total wage cost
- Constraints: enough capacity to meet estimated demand with a safety factor
- Solver: PuLP (Integer Linear Programming)
- Outputs: prints plan + saves 5 visuals to ./downloads/

Why is this prescriptive?
This model recommends an action (how many servers to schedule in each shift) by solving
an optimization problem that balances cost against service capacity requirements.
"""

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Built-in dataset
import seaborn as sns

# Optimization
try:
    import pulp
except ImportError as e:
    raise SystemExit(
        "This script requires 'pulp'. Install it with:\n\n  pip install pulp\n"
    ) from e


# -------------------------
# Config / assumptions
# -------------------------
DAY_ORDER = ["Thur", "Fri", "Sat", "Sun"]
TIME_ORDER = ["Lunch", "Dinner"]

# Capacity assumptions (can be tuned):
CAPACITY_PER_SERVER = 12      # parties a server can handle per shift
SAFETY_FACTOR = 1.15          # buffer on demand to protect service level
WAGE_PER_SERVER_LUNCH = 55.0  # £ per lunch shift
WAGE_PER_SERVER_DINNER = 65.0 # £ per dinner shift


def ensure_dir(path="downloads"):
    os.makedirs(path, exist_ok=True)
    return path


def load_and_prepare():
    df = sns.load_dataset("tips")
    # We treat each row as one "party" that came in.
    # Encode ordered categories for clean display
    df["day"] = pd.Categorical(df["day"], categories=DAY_ORDER, ordered=True)
    df["time"] = pd.Categorical(df["time"], categories=TIME_ORDER, ordered=True)
    # Demand per shift = number of parties observed in dataset for that (day,time)
    demand = (
        df.groupby(["day", "time"])
          .size()
          .rename("parties")
          .reset_index()
          .pivot(index="day", columns="time", values="parties")
          .fillna(0)
          .reindex(index=DAY_ORDER, columns=TIME_ORDER)
    )
    return df, demand


def build_and_solve_lp(demand: pd.DataFrame):
    days = list(demand.index)
    times = list(demand.columns)

    # Decision variables: integer servers[day,time] >= 0
    model = pulp.LpProblem("StaffingOptimization", pulp.LpMinimize)
    servers = pulp.LpVariable.dicts(
        "servers",
        ((d, t) for d in days for t in times),
        lowBound=0,
        cat=pulp.LpInteger
    )

    # Costs per shift
    wage = {(d, "Lunch"): WAGE_PER_SERVER_LUNCH for d in days}
    wage.update({(d, "Dinner"): WAGE_PER_SERVER_DINNER for d in days})

    # Objective: minimize total wage cost
    model += pulp.lpSum(wage[(d, t)] * servers[(d, t)] for d in days for t in times)

    # Capacity constraints: servers * capacity >= SAFETY_FACTOR * demand
    for d in days:
        for t in times:
            req = SAFETY_FACTOR * float(demand.loc[d, t])
            model += servers[(d, t)] * CAPACITY_PER_SERVER >= req, f"capacity_{d}_{t}"

    # Optional: ensure at least 1 server if there is any demand (open shift)
    for d in days:
        for t in times:
            if demand.loc[d, t] > 0:
                model += servers[(d, t)] >= 1, f"min_staff_{d}_{t}"

    # Solve
    _ = model.solve(pulp.PULP_CBC_CMD(msg=False))

    # Collect solution
    sol = pd.DataFrame(
        {(d, t): [int(servers[(d, t)].value())] for d in days for t in times},
        index=["servers"]
    ).T.reset_index()
    sol.columns = ["day", "time", "servers"]
    sol = sol.pivot(index="day", columns="time", values="servers").reindex(index=days, columns=times)

    total_cost = 0.0
    for d in days:
        for t in times:
            total_cost += wage[(d, t)] * sol.loc[d, t]

    return sol, total_cost


# -------------------------
# Visuals
# -------------------------
def fig1_demand_by_shift(demand: pd.DataFrame, outdir: str):
    plt.figure(figsize=(8, 5))
    width = 0.35
    x = np.arange(len(demand.index))
    plt.bar(x - width/2, demand["Lunch"], width, label="Lunch")
    plt.bar(x + width/2, demand["Dinner"], width, label="Dinner")
    plt.title("Observed Parties by Shift (from dataset)")
    plt.xlabel("Day")
    plt.ylabel("Parties")
    plt.xticks(x, demand.index)
    plt.legend()
    plt.tight_layout()
    path = os.path.join(outdir, "01_demand_by_shift.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig2_staffing_plan(servers: pd.DataFrame, outdir: str):
    plt.figure(figsize=(8, 5))
    width = 0.35
    x = np.arange(len(servers.index))
    plt.bar(x - width/2, servers["Lunch"], width, label="Lunch")
    plt.bar(x + width/2, servers["Dinner"], width, label="Dinner")
    plt.title("Optimal Staffing Plan (servers per shift)")
    plt.xlabel("Day")
    plt.ylabel("Servers")
    plt.xticks(x, servers.index)
    plt.legend()
    plt.tight_layout()
    path = os.path.join(outdir, "02_staffing_plan.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig3_capacity_vs_required(demand: pd.DataFrame, servers: pd.DataFrame, outdir: str):
    req = (SAFETY_FACTOR * demand).rename(columns=lambda c: f"Req {c}")
    cap = (CAPACITY_PER_SERVER * servers).rename(columns=lambda c: f"Cap {c}")
    # Plot stacked bars per shift showing required vs capacity (side-by-side groups)
    days = demand.index
    x = np.arange(len(days))
    width = 0.2

    plt.figure(figsize=(10, 5))
    # Lunch required & capacity
    plt.bar(x - width*1.5, req["Req Lunch"], width, label="Required Lunch")
    plt.bar(x - width*0.5, cap["Cap Lunch"], width, label="Capacity Lunch")
    # Dinner required & capacity
    plt.bar(x + width*0.5, req["Req Dinner"], width, label="Required Dinner")
    plt.bar(x + width*1.5, cap["Cap Dinner"], width, label="Capacity Dinner")

    plt.title("Capacity vs Required Demand (with safety factor)")
    plt.xlabel("Day")
    plt.ylabel("Parties")
    plt.xticks(x, days)
    plt.legend(ncol=2)
    plt.tight_layout()
    path = os.path.join(outdir, "03_capacity_vs_required.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig4_utilization_heatmap(demand: pd.DataFrame, servers: pd.DataFrame, outdir: str):
    # Utilization = required / capacity (clip at 1.2 for scale)
    required = SAFETY_FACTOR * demand
    capacity = CAPACITY_PER_SERVER * servers.clip(lower=1)  # avoid divide-by-zero
    util = (required / capacity).replace([np.inf, -np.inf], np.nan).fillna(0).clip(0, 1.2)

    data = util.values
    plt.figure(figsize=(6, 4.5))
    im = plt.imshow(data, aspect="auto")
    plt.title("Utilization (Required / Capacity)")
    plt.xticks(ticks=np.arange(util.shape[1]), labels=util.columns)
    plt.yticks(ticks=np.arange(util.shape[0]), labels=util.index)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            plt.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center")
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Utilization")
    plt.tight_layout()
    path = os.path.join(outdir, "04_utilization_heatmap.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig5_cost_sensitivity(demand: pd.DataFrame, servers: pd.DataFrame, outdir: str):
    """
    Sensitivity of total wage cost to server capacity assumptions.
    For each capacity value, compute required servers = ceil(required / capacity) and cost.
    """
    days = demand.index
    # Wages per shift vector aligned with (day,time)
    wages = []
    for d in days:
        wages.append(WAGE_PER_SERVER_LUNCH)  # Lunch
        wages.append(WAGE_PER_SERVER_DINNER) # Dinner
    wages = np.array(wages)

    req = SAFETY_FACTOR * demand.copy()
    req_vec = np.column_stack([req["Lunch"].values, req["Dinner"].values]).reshape(-1)

    capacities = np.arange(6, 21, 1)  # 6..20 parties/server/shift
    costs = []
    for cap in capacities:
        servers_needed = np.ceil(req_vec / cap)
        total_cost = (servers_needed * wages).sum()
        costs.append(total_cost)

    plt.figure(figsize=(8, 5))
    plt.plot(capacities, costs, marker="o")
    plt.title("Cost Sensitivity to Server Capacity Assumption")
    plt.xlabel("Capacity per Server (parties per shift)")
    plt.ylabel("Total Wage Cost (£)")
    plt.tight_layout()
    path = os.path.join(outdir, "05_cost_sensitivity.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


# -------------------------
# Main
# -------------------------
def main():
    outdir = ensure_dir("downloads")
    df, demand = load_and_prepare()

    servers, total_cost = build_and_solve_lp(demand)

    # Print plan
    print("\n=== Prescriptive Staffing Plan (servers per shift) ===")
    print(servers.fillna(0).astype(int))
    print(f"\nTotal wage cost: £{total_cost:,.2f}")
    print(f"Assumptions -> capacity/server: {CAPACITY_PER_SERVER} parties/shift, safety factor: {SAFETY_FACTOR}")

    # Save visuals
    print("\nSaving visuals locally to:", os.path.abspath(outdir), "\n")
    saved = []
    saved.append(fig1_demand_by_shift(demand, outdir))
    saved.append(fig2_staffing_plan(servers, outdir))
    saved.append(fig3_capacity_vs_required(demand, servers, outdir))
    saved.append(fig4_utilization_heatmap(demand, servers, outdir))
    saved.append(fig5_cost_sensitivity(demand, servers, outdir))

    print("✅ Visuals saved:")
    for p in saved:
        print(" -", os.path.abspath(p))

    # Short explanation of why this is prescriptive
    print("\nWhy prescriptive?")
    print("This model recommends the number of servers to schedule in each shift that minimizes wage cost")
    print("while satisfying capacity constraints derived from data (demand × safety factor).")
    print("It prescribes an optimal action (staffing levels), not just describing or predicting outcomes.")


if __name__ == "__main__":
    main()
