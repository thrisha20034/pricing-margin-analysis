-- 01_create_tables.sql
-- Creates the core tables for the pricing analysis project.

CREATE TABLE IF NOT EXISTS orders (
    order_id        TEXT,
    order_date      DATE,
    ship_date       DATE,
    ship_mode       TEXT,
    customer_id     TEXT,
    customer_name   TEXT,
    segment         TEXT,
    country         TEXT,
    city            TEXT,
    state           TEXT,
    region          TEXT,
    product_id      TEXT,
    category        TEXT,
    sub_category    TEXT,
    product_name    TEXT,
    sales           REAL,
    quantity        INTEGER,
    discount        REAL,
    profit          REAL
);

-- Derived table for margin analysis
CREATE TABLE IF NOT EXISTS pricing_features AS
SELECT
    order_id,
    order_date,
    category,
    sub_category,
    product_name,
    segment,
    region,
    sales,
    quantity,
    discount,
    profit,

    -- Margin %
    CASE
        WHEN sales != 0 THEN ROUND((profit / sales) * 100, 2)
        ELSE NULL
    END AS margin_pct,

    -- Discount band
    CASE
        WHEN discount = 0             THEN 'No Discount'
        WHEN discount <= 0.10         THEN 'Low (1-10%)'
        WHEN discount <= 0.20         THEN 'Medium (11-20%)'
        ELSE                               'High (>20%)'
    END AS discount_band,

    -- Profitability flag
    CASE WHEN profit > 0 THEN 1 ELSE 0 END AS is_profitable,

    -- Unit economics
    ROUND(sales / quantity, 2)   AS revenue_per_unit,
    ROUND(profit / quantity, 2)  AS profit_per_unit

FROM orders
WHERE sales IS NOT NULL
  AND profit IS NOT NULL
  AND discount IS NOT NULL
  AND quantity IS NOT NULL;
