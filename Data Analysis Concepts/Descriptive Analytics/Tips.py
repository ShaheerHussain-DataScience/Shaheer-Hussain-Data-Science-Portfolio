#!/usr/bin/env python3
"""
Descriptive analytics on Seaborn's 'tips' dataset with 5 visuals.

- Prints overall summary stats and group summaries
- Saves figures to ./figures/
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Only used to load the built-in dataset
import seaborn as sns


def ensure_dir(path="figures"):
    os.makedirs(path, exist_ok=True)
    return path


def load_data():
    df = sns.load_dataset("tips")
    # Derive a useful metric: tip percentage
    df["tip_pct"] = df["tip"] / df["total_bill"] * 100
    # Make categorical orders explicit for nicer plots
    day_order = ["Thur", "Fri", "Sat", "Sun"]
    time_order = ["Lunch", "Dinner"]
    df["day"] = pd.Categorical(df["day"], categories=day_order, ordered=True)
    df["time"] = pd.Categorical(df["time"], categories=time_order, ordered=True)
    return df


def print_descriptives(df: pd.DataFrame):
    print("\n=== Overall numeric summary ===")
    print(df[["total_bill", "tip", "size", "tip_pct"]].describe().round(2))

    print("\n=== Category counts ===")
    for col in ["sex", "smoker", "day", "time"]:
        print(f"\n{col} value counts:")
        print(df[col].value_counts())

    print("\n=== Average tip % by day ===")
    print(df.groupby("day")["tip_pct"].mean().round(2))

    print("\n=== Average bill and tip by time ===")
    print(df.groupby("time")[["total_bill", "tip"]].mean().round(2))

    print("\n=== Average tip % by smoker status and time ===")
    print(df.pivot_table(values="tip_pct", index="smoker", columns="time", aggfunc="mean").round(2))


def fig1_hist_total_bill(df: pd.DataFrame, outdir: str):
    plt.figure(figsize=(8, 5))
    plt.hist(df["total_bill"], bins=30)
    plt.title("Distribution of Total Bill")
    plt.xlabel("Total Bill ($)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    path = os.path.join(outdir, "01_hist_total_bill.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig2_box_tip_pct_by_day(df: pd.DataFrame, outdir: str):
    # Using pandas' built-in boxplot (matplotlib under the hood)
    plt.figure(figsize=(8, 5))
    df.boxplot(column="tip_pct", by="day")
    plt.suptitle("")  # remove automatic suptitle
    plt.title("Tip Percentage by Day")
    plt.xlabel("Day")
    plt.ylabel("Tip %")
    plt.tight_layout()
    path = os.path.join(outdir, "02_box_tip_pct_by_day.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig3_bar_mean_tip_pct_by_day(df: pd.DataFrame, outdir: str):
    means = df.groupby("day")["tip_pct"].mean().reindex(df["day"].cat.categories)
    plt.figure(figsize=(8, 5))
    means.plot(kind="bar")
    plt.title("Average Tip % by Day")
    plt.xlabel("Day")
    plt.ylabel("Average Tip %")
    for i, v in enumerate(means):
        plt.text(i, v, f"{v:.1f}%", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    path = os.path.join(outdir, "03_bar_mean_tip_pct_by_day.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig4_scatter_bill_vs_tip_with_trend(df: pd.DataFrame, outdir: str):
    x = df["total_bill"].values
    y = df["tip"].values
    # Simple linear trendline
    coeffs = np.polyfit(x, y, 1)
    trend = np.poly1d(coeffs)

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, alpha=0.7)
    xs = np.linspace(x.min(), x.max(), 100)
    plt.plot(xs, trend(xs), linewidth=2)
    plt.title("Tip vs Total Bill with Trendline")
    plt.xlabel("Total Bill ($)")
    plt.ylabel("Tip ($)")
    eq = f"y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}"
    plt.text(0.05, 0.95, eq, transform=plt.gca().transAxes, ha="left", va="top")
    plt.tight_layout()
    path = os.path.join(outdir, "04_scatter_tip_vs_bill_trend.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def fig5_heatmap_tip_pct_by_day_time(df: pd.DataFrame, outdir: str):
    pivot = df.pivot_table(values="tip_pct", index="day", columns="time", aggfunc="mean")
    data = pivot.values
    plt.figure(figsize=(6, 5))
    im = plt.imshow(data, aspect="auto")
    plt.title("Average Tip % by Day and Time")
    plt.xticks(ticks=np.arange(pivot.shape[1]), labels=pivot.columns)
    plt.yticks(ticks=np.arange(pivot.shape[0]), labels=pivot.index)
    # Annotate cells
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            plt.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center")
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Tip %")
    plt.tight_layout()
    path = os.path.join(outdir, "05_heatmap_tip_pct_by_day_time.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def main(show: bool = False):
    outdir = ensure_dir("figures")
    df = load_data()
    print_descriptives(df)

    paths = []
    paths.append(fig1_hist_total_bill(df, outdir))
    paths.append(fig2_box_tip_pct_by_day(df, outdir))
    paths.append(fig3_bar_mean_tip_pct_by_day(df, outdir))
    paths.append(fig4_scatter_bill_vs_tip_with_trend(df, outdir))
    paths.append(fig5_heatmap_tip_pct_by_day_time(df, outdir))

    print("\nSaved figures:")
    for p in paths:
        print(f" - {p}")

    if show:
        # Optional interactive display if running locally
        for p in paths:
            img = plt.imread(p)
            plt.figure()
            plt.imshow(img)
            plt.axis("off")
            plt.title(os.path.basename(p))
        plt.show()


if __name__ == "__main__":
    # Set show=True to pop up the images when running locally
    main(show=False)
