# Dashboard Setup Guide

This guide explains how to build the Pricing & Margin Analysis dashboard in **Tableau Public** (free) or **Power BI Desktop** (free).

---

## Data Sources

Connect to the following files from `data/processed/` after running the Python pipeline:

| File | Use |
|---|---|
| `pricing_clean.csv` | Main transaction-level dataset |
| `subcategory_margin.csv` | Margin by sub-category |
| `discount_effectiveness.csv` | Discount band impact |
| `monthly_margin_trend.csv` | Time-series trend data |

---

## Recommended Dashboard Pages

### Page 1 — Overview

**Metric cards (top row):**
- Total Revenue
- Total Profit
- Overall Margin %
- % of Unprofitable Orders

**Charts:**
- Bar chart: Margin % by Category
- Treemap: Revenue contribution by Sub-Category

---

### Page 2 — Discount Impact

**Charts:**
- Grouped bar chart: Avg Margin % by Discount Band (color: green = positive, red = negative)
- Scatter plot: Discount % (x-axis) vs Margin % (y-axis), colored by Sub-Category
- Table: Top 10 products with highest discount and lowest margin

**Filter:** Segment selector (Consumer / Corporate / Home Office)

---

### Page 3 — Category Deep Dive

**Charts:**
- Heatmap: Sub-Category (rows) × Discount Band (columns), cell value = Avg Margin %
- Bar chart: Revenue vs Profit side by side, by Sub-Category

**Filter:** Category selector

---

### Page 4 — Trend Analysis

**Charts:**
- Line chart: Monthly Revenue and Margin % over time (dual axis)
- Line chart: Margin % by Category over time

---

## Tableau Quick Start

1. Open Tableau Public → Connect → Text File → select `pricing_clean.csv`
2. Drag `Discount Band` to Columns, `Margin Pct` to Rows
3. Change mark type to Bar
4. Drag `Is Profitable` to Color for instant red/green split
5. Add `Category` and `Sub Category` as filters

---

## Power BI Quick Start

1. Open Power BI Desktop → Get Data → Text/CSV → select `pricing_clean.csv`
2. Transform Data: verify `discount` is decimal, `margin_pct` is decimal
3. Add a Card visual → drag `margin_pct` with Average aggregation
4. Add a Bar Chart: X = `discount_band`, Y = Average of `margin_pct`
5. Add a Line Chart: X = `order_month`, Y = Sum of `sales` and Sum of `profit`

---

## Suggested Color Scheme

| Meaning | Color |
|---|---|
| Positive margin / profitable | `#1D9E75` (teal green) |
| Negative margin / loss | `#D85A30` (coral red) |
| Neutral / No discount | `#378ADD` (blue) |
| Background / labels | `#F1EFE8` (light gray) |
