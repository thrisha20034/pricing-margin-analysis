"""
margin_analysis.py
------------------
Loads processed data and runs pricing & margin analysis.
Outputs findings to the console and saves result tables.

Usage:
    python scripts/margin_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

CLEAN_PATH = "data/processed/pricing_clean.csv"
OUTPUT_DIR = "data/processed"


def load_clean_data() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_PATH, encoding="latin-1")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    return df


# ─── Analysis 1: Margin by Category & Sub-Category ───────────────────────────

def margin_by_category(df: pd.DataFrame):
    print("\n=== Margin % by Category ===")
    cat = (
        df.groupby("category")
        .agg(avg_margin=("margin_pct", "mean"), total_profit=("profit", "sum"), total_sales=("sales", "sum"))
        .assign(margin_pct=lambda x: (x["total_profit"] / x["total_sales"] * 100).round(2))
        .sort_values("margin_pct", ascending=False)
    )
    print(cat[["margin_pct", "total_sales", "total_profit"]].to_string())

    print("\n=== Top 5 and Bottom 5 Sub-Categories by Margin ===")
    sub = (
        df.groupby(["category", "sub_category"])
        .agg(total_profit=("profit", "sum"), total_sales=("sales", "sum"))
        .assign(margin_pct=lambda x: (x["total_profit"] / x["total_sales"] * 100).round(2))
        .sort_values("margin_pct", ascending=False)
        .reset_index()
    )
    print("Top 5:")
    print(sub.head(5)[["category", "sub_category", "margin_pct", "total_sales"]].to_string(index=False))
    print("\nBottom 5:")
    print(sub.tail(5)[["category", "sub_category", "margin_pct", "total_sales"]].to_string(index=False))

    sub.to_csv(f"{OUTPUT_DIR}/subcategory_margin.csv", index=False)
    return sub


# ─── Analysis 2: Discount Effectiveness ──────────────────────────────────────

def discount_effectiveness(df: pd.DataFrame):
    print("\n=== Discount Band vs. Margin ===")
    band = (
        df.groupby("discount_band")
        .agg(
            avg_margin=("margin_pct", "mean"),
            avg_discount=("discount", "mean"),
            order_count=("order_id", "count"),
            unprofitable=("is_profitable", lambda x: (~x).sum()),
            total_revenue=("sales", "sum"),
        )
        .assign(
            unprofitable_rate=lambda x: (x["unprofitable"] / x["order_count"] * 100).round(1),
            avg_discount_pct=lambda x: (x["avg_discount"] * 100).round(1),
            avg_margin=lambda x: x["avg_margin"].round(2),
        )
    )
    print(band[["avg_discount_pct", "avg_margin", "order_count", "unprofitable_rate", "total_revenue"]].to_string())
    band.to_csv(f"{OUTPUT_DIR}/discount_effectiveness.csv")

    # Key insight
    high = band.loc["High (>20%)", "avg_margin"] if "High (>20%)" in band.index else None
    none = band.loc["No Discount", "avg_margin"] if "No Discount" in band.index else None
    if high and none:
        print(f"\n  ⚠  High-discount orders average {high:.1f}% margin vs {none:.1f}% for no-discount orders.")

    return band


# ─── Analysis 3: Price Sensitivity by Segment ────────────────────────────────

def price_sensitivity_by_segment(df: pd.DataFrame):
    print("\n=== Price Sensitivity: Segment × Discount Band ===")
    seg = (
        df.groupby(["segment", "discount_band"])
        .agg(avg_margin=("margin_pct", "mean"), order_count=("order_id", "count"))
        .assign(avg_margin=lambda x: x["avg_margin"].round(2))
        .reset_index()
    )
    pivot = seg.pivot(index="segment", columns="discount_band", values="avg_margin")
    print(pivot.to_string())
    seg.to_csv(f"{OUTPUT_DIR}/segment_price_sensitivity.csv", index=False)
    return seg


# ─── Analysis 4: Revenue & Margin Trend Over Time ────────────────────────────

def margin_trend(df: pd.DataFrame):
    print("\n=== Monthly Margin Trend (last 12 months of data) ===")
    monthly = (
        df.groupby("order_month")
        .agg(total_sales=("sales", "sum"), total_profit=("profit", "sum"))
        .assign(margin_pct=lambda x: (x["total_profit"] / x["total_sales"] * 100).round(2))
        .reset_index()
        .sort_values("order_month")
        .tail(12)
    )
    print(monthly[["order_month", "total_sales", "total_profit", "margin_pct"]].to_string(index=False))
    monthly.to_csv(f"{OUTPUT_DIR}/monthly_margin_trend.csv", index=False)
    return monthly


# ─── Analysis 5: Heavy Discounting / Low Margin Products ──────────────────────

def find_problematic_products(df: pd.DataFrame):
    print("\n=== Products: High Discount, Low/Negative Margin ===")
    prod = (
        df.groupby(["category", "sub_category", "product_name"])
        .agg(
            avg_discount=("discount", "mean"),
            avg_margin=("margin_pct", "mean"),
            total_profit=("profit", "sum"),
            order_count=("order_id", "count"),
        )
        .assign(
            avg_discount_pct=lambda x: (x["avg_discount"] * 100).round(1),
            avg_margin=lambda x: x["avg_margin"].round(2),
        )
        .reset_index()
    )

    # Products with >20% discount AND negative average margin
    problem = prod[(prod["avg_discount_pct"] > 20) & (prod["avg_margin"] < 0)].sort_values("avg_margin")
    print(f"  Found {len(problem)} products with >20% avg discount and negative margin.")
    print(problem[["sub_category", "product_name", "avg_discount_pct", "avg_margin", "total_profit"]].head(10).to_string(index=False))
    problem.to_csv(f"{OUTPUT_DIR}/problematic_products.csv", index=False)
    return problem


# ─── Plot: Discount Band vs Margin ───────────────────────────────────────────

def plot_discount_vs_margin(df: pd.DataFrame):
    band_order = ["No Discount", "Low (1-10%)", "Medium (11-20%)", "High (>20%)"]
    band = (
        df.groupby("discount_band")
        .agg(avg_margin=("margin_pct", "mean"))
        .reindex(band_order)
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["#1D9E75" if m > 0 else "#D85A30" for m in band["avg_margin"]]
    bars = ax.bar(band.index, band["avg_margin"], color=colors, width=0.5)
    ax.axhline(0, color="#888780", linewidth=0.8, linestyle="--")
    ax.set_title("Average Margin % by Discount Band", fontsize=13, fontweight="bold")
    ax.set_xlabel("Discount Band")
    ax.set_ylabel("Avg Margin %")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))

    for bar, val in zip(bars, band["avg_margin"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (0.3 if val >= 0 else -1.2),
            f"{val:.1f}%",
            ha="center", va="bottom", fontsize=10
        )

    plt.tight_layout()
    os.makedirs("data/processed", exist_ok=True)
    plt.savefig("data/processed/discount_margin_chart.png", dpi=150)
    print("\n  Chart saved → data/processed/discount_margin_chart.png")
    plt.show()


def main():
    print("Loading processed data...")
    df = load_clean_data()
    print(f"  {len(df):,} rows loaded.\n")

    margin_by_category(df)
    discount_effectiveness(df)
    price_sensitivity_by_segment(df)
    margin_trend(df)
    find_problematic_products(df)
    plot_discount_vs_margin(df)

    print("\nAll analyses complete. Results saved to data/processed/")


if __name__ == "__main__":
    main()
