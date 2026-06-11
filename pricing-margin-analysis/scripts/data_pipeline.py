"""
data_pipeline.py
----------------
Reads raw Superstore CSV, cleans and transforms it,
and outputs processed files ready for analysis.

Usage:
    python scripts/data_pipeline.py
"""

import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw/superstore.csv"
CLEAN_PATH = "data/processed/pricing_clean.csv"
SUMMARY_PATH = "data/processed/margin_summary.csv"


def load_data(path: str) -> pd.DataFrame:
    print(f"Loading data from {path}...")
    df = pd.read_csv(path, encoding="latin-1")
    print(f"  Loaded {len(df):,} rows, {df.shape[1]} columns.")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning data...")

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"  Removed {before - len(df)} duplicate rows.")

    # Drop rows missing key fields
    key_cols = ["sales", "profit", "discount", "quantity"]
    df = df.dropna(subset=key_cols)

    # Fix data types
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce")
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Clip discount to valid range [0, 1]
    df["discount"] = df["discount"].clip(0, 1)

    print(f"  Clean dataset: {len(df):,} rows remaining.")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    print("Engineering features...")

    # Core margin metric
    df["margin_pct"] = np.where(
        df["sales"] != 0,
        (df["profit"] / df["sales"]) * 100,
        np.nan
    )

    # Unit economics
    df["revenue_per_unit"] = df["sales"] / df["quantity"]
    df["profit_per_unit"] = df["profit"] / df["quantity"]

    # Discount bands
    bins = [-0.001, 0.0, 0.10, 0.20, 1.0]
    labels = ["No Discount", "Low (1-10%)", "Medium (11-20%)", "High (>20%)"]
    df["discount_band"] = pd.cut(df["discount"], bins=bins, labels=labels)

    # Profitability flag
    df["is_profitable"] = df["profit"] > 0

    # Year and month for trend analysis
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    print("  Features added: margin_pct, discount_band, is_profitable, revenue_per_unit, profit_per_unit")
    return df


def build_margin_summary(df: pd.DataFrame) -> pd.DataFrame:
    print("Building margin summary by sub-category...")

    summary = (
        df.groupby(["category", "sub_category", "discount_band"])
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            avg_margin_pct=("margin_pct", "mean"),
            avg_discount=("discount", "mean"),
            order_count=("order_id", "count"),
            unprofitable_orders=("is_profitable", lambda x: (~x).sum()),
        )
        .reset_index()
    )

    summary["unprofitable_rate_pct"] = (
        summary["unprofitable_orders"] / summary["order_count"] * 100
    ).round(1)

    summary["avg_margin_pct"] = summary["avg_margin_pct"].round(2)
    summary["avg_discount"] = (summary["avg_discount"] * 100).round(1)
    summary["total_sales"] = summary["total_sales"].round(2)
    summary["total_profit"] = summary["total_profit"].round(2)

    return summary


def save_outputs(df: pd.DataFrame, summary: pd.DataFrame):
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)
    print(f"\nSaved cleaned data → {CLEAN_PATH}")
    print(f"Saved margin summary → {SUMMARY_PATH}")


def print_quick_stats(df: pd.DataFrame):
    print("\n--- Quick Stats ---")
    print(f"Total orders:        {len(df):,}")
    print(f"Total revenue:       ${df['sales'].sum():,.0f}")
    print(f"Total profit:        ${df['profit'].sum():,.0f}")
    print(f"Overall margin:      {df['profit'].sum() / df['sales'].sum() * 100:.1f}%")
    print(f"Unprofitable orders: {(~df['is_profitable']).sum():,} ({(~df['is_profitable']).mean()*100:.1f}%)")
    print()
    print("Avg margin by discount band:")
    band_stats = df.groupby("discount_band")["margin_pct"].mean().round(1)
    for band, margin in band_stats.items():
        print(f"  {band:<20} {margin:>6.1f}%")


def main():
    df = load_data(RAW_PATH)
    df = clean_data(df)
    df = engineer_features(df)
    summary = build_margin_summary(df)
    save_outputs(df, summary)
    print_quick_stats(df)
    print("\nPipeline complete.")


if __name__ == "__main__":
    main()
