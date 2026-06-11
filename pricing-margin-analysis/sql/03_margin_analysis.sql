-- 03_margin_analysis.sql
-- Core pricing and margin analysis queries.
-- Run these after 01_create_tables.sql and 02_data_cleaning.sql.


-- ─── Query 1: Margin % by Category ──────────────────────────────────────────

SELECT
    category,
    ROUND(SUM(profit) / SUM(sales) * 100, 2)   AS margin_pct,
    ROUND(SUM(sales), 0)                         AS total_revenue,
    ROUND(SUM(profit), 0)                        AS total_profit,
    COUNT(*)                                     AS order_count
FROM pricing_features
GROUP BY category
ORDER BY margin_pct DESC;


-- ─── Query 2: Margin % by Sub-Category ──────────────────────────────────────

SELECT
    category,
    sub_category,
    ROUND(SUM(profit) / SUM(sales) * 100, 2)   AS margin_pct,
    ROUND(SUM(sales), 0)                         AS total_revenue,
    ROUND(SUM(profit), 0)                        AS total_profit,
    COUNT(*)                                     AS order_count
FROM pricing_features
GROUP BY category, sub_category
ORDER BY margin_pct DESC;


-- ─── Query 3: Discount Band Impact on Margin ─────────────────────────────────

SELECT
    discount_band,
    ROUND(AVG(discount) * 100, 1)              AS avg_discount_pct,
    ROUND(AVG(margin_pct), 2)                  AS avg_margin_pct,
    ROUND(SUM(sales), 0)                        AS total_revenue,
    COUNT(*)                                    AS order_count,
    SUM(CASE WHEN is_profitable = 0 THEN 1 ELSE 0 END) AS unprofitable_orders,
    ROUND(
        SUM(CASE WHEN is_profitable = 0 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1
    )                                           AS unprofitable_rate_pct
FROM pricing_features
GROUP BY discount_band
ORDER BY avg_discount_pct;


-- ─── Query 4: Discount Effectiveness (Revenue lift per discount tier) ─────────

SELECT
    sub_category,
    discount_band,
    ROUND(AVG(revenue_per_unit), 2)            AS avg_revenue_per_unit,
    ROUND(AVG(margin_pct), 2)                  AS avg_margin_pct,
    COUNT(*)                                   AS order_count
FROM pricing_features
GROUP BY sub_category, discount_band
ORDER BY sub_category, avg_discount_pct;


-- ─── Query 5: Price Sensitivity — Segment × Discount Band ───────────────────

SELECT
    segment,
    discount_band,
    ROUND(AVG(margin_pct), 2)  AS avg_margin_pct,
    ROUND(AVG(discount)*100,1) AS avg_discount_pct,
    COUNT(*)                   AS order_count
FROM pricing_features
GROUP BY segment, discount_band
ORDER BY segment, avg_discount_pct;


-- ─── Query 6: High Discount, Low/Negative Margin Products ────────────────────

SELECT
    category,
    sub_category,
    product_name,
    ROUND(AVG(discount) * 100, 1)   AS avg_discount_pct,
    ROUND(AVG(margin_pct), 2)       AS avg_margin_pct,
    ROUND(SUM(profit), 0)           AS total_profit,
    COUNT(*)                        AS order_count
FROM pricing_features
WHERE discount > 0.20
GROUP BY category, sub_category, product_name
HAVING avg_margin_pct < 0
ORDER BY avg_margin_pct ASC
LIMIT 20;


-- ─── Query 7: Monthly Revenue & Margin Trend ─────────────────────────────────

SELECT
    STRFTIME('%Y-%m', order_date)              AS order_month,
    ROUND(SUM(sales), 0)                       AS total_revenue,
    ROUND(SUM(profit), 0)                      AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2)  AS margin_pct,
    COUNT(*)                                   AS order_count
FROM pricing_features
GROUP BY order_month
ORDER BY order_month;


-- ─── Query 8: Category Revenue Contribution % ────────────────────────────────

SELECT
    category,
    ROUND(SUM(sales), 0)                                             AS category_revenue,
    ROUND(SUM(sales) / SUM(SUM(sales)) OVER () * 100, 1)            AS revenue_share_pct,
    ROUND(SUM(profit) / SUM(SUM(profit)) OVER () * 100, 1)          AS profit_share_pct
FROM pricing_features
GROUP BY category
ORDER BY category_revenue DESC;
