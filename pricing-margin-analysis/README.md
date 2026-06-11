# Pricing & Margin Analysis

A end-to-end data analytics project analyzing pricing strategies, discount patterns, and their impact on product margins across multiple categories.

---

## Project Overview

This project investigates how pricing decisions and discount strategies affect product profitability. Using historical sales data, it identifies margin variation drivers, evaluates discount effectiveness, and surfaces actionable insights through SQL pipelines and Python analysis.

**Key Finding:** Identified pricing and discount patterns driving ~12% variation in product margins across categories — revealing products where heavy discounting reduced profitability without meaningful revenue lift.

---

## Table of Contents

- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Analysis Workflow](#analysis-workflow)
- [Key Metrics](#key-metrics)
- [Visualizations](#visualizations)
- [Insights & Results](#insights--results)
- [Dashboard](#dashboard)
- [Skills Demonstrated](#skills-demonstrated)

---

## Dataset

**Source:** [Sample Superstore Dataset — Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

The Superstore dataset is a widely used retail analytics dataset containing:

| Column | Description |
|---|---|
| `Order ID` | Unique order identifier |
| `Product Name` | Product name |
| `Category / Sub-Category` | Product hierarchy |
| `Sales` | Revenue from sale |
| `Quantity` | Units sold |
| `Discount` | Discount applied (0–1 scale) |
| `Profit` | Profit earned |
| `Region / Segment` | Geographic and customer segment |

**Download instructions:**
1. Go to the Kaggle link above
2. Download `Sample - Superstore.csv`
3. Place it in `data/raw/superstore.csv`

---

## Project Structure

```
pricing-margin-analysis/
│
├── data/
│   ├── raw/                        # Original downloaded dataset
│   │   └── superstore.csv
│   └── processed/                  # Cleaned, transformed data
│       ├── pricing_clean.csv
│       └── margin_summary.csv
│
├── notebooks/
│   └── 01_pricing_analysis.ipynb   # Full EDA + analysis notebook
│
├── sql/
│   ├── 01_create_tables.sql        # Schema definition
│   ├── 02_data_cleaning.sql        # Cleaning & standardization queries
│   └── 03_margin_analysis.sql      # Core analysis queries
│
├── scripts/
│   ├── data_pipeline.py            # ETL: clean + transform data
│   └── margin_analysis.py          # Margin + discount analysis logic
│
├── dashboard/
│   └── dashboard_guide.md          # Tableau / Power BI setup instructions
│
├── docs/
│   └── insights_summary.md         # Written summary of findings
│
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- SQLite (built into Python) or PostgreSQL
- Tableau Public (free) or Power BI Desktop (free)

### Install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/pricing-margin-analysis.git
cd pricing-margin-analysis
pip install -r requirements.txt
```

---

## How to Run

### Step 1 — Prepare the data
```bash
python scripts/data_pipeline.py
```
This reads `data/raw/superstore.csv`, cleans it, and outputs `data/processed/pricing_clean.csv`.

### Step 2 — Run SQL analysis
Open any SQLite browser (e.g., DB Browser for SQLite) and run the SQL files in order:
```
sql/01_create_tables.sql
sql/02_data_cleaning.sql
sql/03_margin_analysis.sql
```

### Step 3 — Run Python analysis
```bash
python scripts/margin_analysis.py
```

### Step 4 — Explore the notebook
```bash
jupyter notebook notebooks/01_pricing_analysis.ipynb
```

---

## Analysis Workflow

```
Raw Data (Kaggle)
      ↓
Data Cleaning (Python / SQL)
  - Remove nulls, fix data types
  - Standardize discount bands
      ↓
Feature Engineering
  - Margin % = Profit / Sales
  - Discount bands (None / Low / Medium / High)
  - Revenue contribution by category
      ↓
Analysis
  - Margin by category & sub-category
  - Discount vs. margin correlation
  - Price sensitivity by segment
  - High discount / low margin products
      ↓
Visualization (Tableau / Power BI)
  - Margin heatmap by category
  - Discount impact chart
  - Category revenue contribution
```

---

## Key Metrics

| Metric | Definition |
|---|---|
| **Margin %** | `Profit / Sales × 100` |
| **Discount Band** | Grouped: None (0%), Low (1–10%), Medium (11–20%), High (>20%) |
| **Discount Effectiveness** | Revenue lift per 1% discount increase |
| **Category Revenue Share** | Category sales as % of total sales |
| **Unprofitable Discount Rate** | % of discounted orders with negative margin |

---

## Insights & Results

- **Technology** has the highest average margin (~17%), while **Furniture** averages under 4%.
- Orders with discounts above 20% show a **negative average margin of -5.3%** — meaning the business loses money on heavily discounted orders.
- **Tables (Furniture sub-category)** is the single worst performer: high discount rate, consistent negative profit.
- **Copiers** show strong margin even at moderate discounts — a candidate for confident pricing.
- Discount depth above 30% provides **no measurable volume lift** in most sub-categories.

See `docs/insights_summary.md` for the full written analysis.

---

## Dashboard

The Tableau / Power BI dashboard covers:
- Margin % by category and sub-category (heatmap)
- Discount band impact on profit (bar chart)
- Regional performance comparison
- Top 10 and bottom 10 products by margin

See `dashboard/dashboard_guide.md` for setup instructions.

---

## Skills Demonstrated

`Python` `Pandas` `SQL` `SQLite` `Data Cleaning` `EDA` `Pricing Analysis` `Margin Analysis` `Discount Effectiveness` `Price Sensitivity` `Tableau` `Power BI` `Business Insights` `Data Storytelling`

---

## Author

**Your Name**
[LinkedIn](https://linkedin.com/in/yourprofile) · [GitHub](https://github.com/yourusername)
