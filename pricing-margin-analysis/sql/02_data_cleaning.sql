-- 02_data_cleaning.sql
-- Validates and standardizes the raw orders table before analysis.

-- Check for nulls in key columns
SELECT
    SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END)    AS null_sales,
    SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END)   AS null_profit,
    SUM(CASE WHEN discount IS NULL THEN 1 ELSE 0 END) AS null_discount,
    SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END) AS null_quantity
FROM orders;

-- Check discount range (should be 0 to 1)
SELECT
    MIN(discount) AS min_discount,
    MAX(discount) AS max_discount,
    AVG(discount) AS avg_discount
FROM orders;

-- Check for negative sales (data quality issue)
SELECT COUNT(*) AS negative_sales_count
FROM orders
WHERE sales < 0;

-- Check for duplicate order + product combinations
SELECT order_id, product_id, COUNT(*) AS cnt
FROM orders
GROUP BY order_id, product_id
HAVING cnt > 1
LIMIT 10;

-- Standardize segment labels (trim whitespace)
UPDATE orders
SET segment = TRIM(segment);

-- Standardize category labels
UPDATE orders
SET category = TRIM(category),
    sub_category = TRIM(sub_category);
