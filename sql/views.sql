USE ecommerce_analytics;

-- ─────────────────────────────────────────────────────────────
-- 1. Monthly Revenue
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_monthly_revenue AS
SELECT
    DATE_FORMAT(p.payment_date, '%Y-%m')        AS month,
    COUNT(DISTINCT o.order_id)                  AS total_orders,
    COUNT(DISTINCT o.customer_id)               AS unique_customers,
    ROUND(SUM(p.amount), 2)                     AS gross_revenue,
    ROUND(AVG(p.amount), 2)                     AS avg_order_value
FROM payments p
JOIN orders   o ON o.order_id = p.order_id
WHERE o.status = 'delivered'
GROUP BY DATE_FORMAT(p.payment_date, '%Y-%m')
ORDER BY month;

-- ─────────────────────────────────────────────────────────────
-- 2. Product Category Performance
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_category_performance AS
SELECT
    pr.category,
    COUNT(DISTINCT oi.order_id)                                             AS total_orders,
    SUM(oi.quantity)                                                        AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount / 100)), 2)   AS revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - pr.cost) * (1 - oi.discount / 100)), 2) AS gross_profit,
    ROUND(AVG(oi.unit_price), 2)                                            AS avg_unit_price
FROM order_items oi
JOIN products    pr ON pr.product_id = oi.product_id
JOIN orders       o ON  o.order_id   = oi.order_id
WHERE o.status = 'delivered'
GROUP BY pr.category
ORDER BY revenue DESC;

-- ─────────────────────────────────────────────────────────────
-- 3. Top Products
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_top_products AS
SELECT
    pr.product_name,
    pr.category,
    SUM(oi.quantity)                                                        AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount / 100)), 2)   AS revenue
FROM order_items oi
JOIN products pr ON pr.product_id = oi.product_id
JOIN orders    o ON  o.order_id   = oi.order_id
WHERE o.status = 'delivered'
GROUP BY pr.product_id, pr.product_name, pr.category
ORDER BY revenue DESC;

-- ─────────────────────────────────────────────────────────────
-- 4. Customer Cohort Analysis (month of first purchase)
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_customer_cohorts AS
WITH first_order AS (
    SELECT customer_id, MIN(order_date) AS first_order_date
    FROM orders
    WHERE status = 'delivered'
    GROUP BY customer_id
)
SELECT
    DATE_FORMAT(fo.first_order_date, '%Y-%m')   AS cohort_month,
    DATE_FORMAT(o.order_date, '%Y-%m')           AS order_month,
    COUNT(DISTINCT o.customer_id)               AS active_customers,
    ROUND(SUM(p.amount), 2)                     AS cohort_revenue
FROM orders      o
JOIN first_order fo ON fo.customer_id   = o.customer_id
JOIN payments     p ON  p.order_id      = o.order_id
WHERE o.status = 'delivered'
GROUP BY cohort_month, order_month
ORDER BY cohort_month, order_month;

-- ─────────────────────────────────────────────────────────────
-- 5. RFM Segmentation (Recency · Frequency · Monetary)
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_rfm AS
WITH rfm_raw AS (
    SELECT
        o.customer_id,
        DATEDIFF(CURDATE(), MAX(o.order_date))  AS recency_days,
        COUNT(DISTINCT o.order_id)              AS frequency,
        ROUND(SUM(p.amount), 2)                 AS monetary
    FROM orders   o
    JOIN payments p ON p.order_id = o.order_id
    WHERE o.status = 'delivered'
    GROUP BY o.customer_id
),
rfm_scored AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency_days ASC)  AS r_score,
        NTILE(5) OVER (ORDER BY frequency    DESC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary     DESC) AS m_score
    FROM rfm_raw
)
SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score)   AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3                   THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2                   THEN 'Recent Customers'
        WHEN r_score <= 2 AND f_score >= 3                   THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score >= 3  THEN 'Cant Lose Them'
        WHEN r_score <= 1                                    THEN 'Lost'
        ELSE 'Potential Loyalists'
    END AS segment
FROM rfm_scored;

-- ─────────────────────────────────────────────────────────────
-- 6. Payment Method Breakdown
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_payment_methods AS
SELECT
    method,
    COUNT(*)                AS transactions,
    ROUND(SUM(amount), 2)   AS total_amount,
    ROUND(AVG(amount), 2)   AS avg_amount
FROM payments
GROUP BY method
ORDER BY total_amount DESC;

-- ─────────────────────────────────────────────────────────────
-- 7. City / State Revenue
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_geo_revenue AS
SELECT
    c.state,
    c.city,
    COUNT(DISTINCT o.order_id)  AS orders,
    ROUND(SUM(p.amount), 2)     AS revenue
FROM customers c
JOIN orders    o ON o.customer_id = c.customer_id
JOIN payments  p ON p.order_id    = o.order_id
WHERE o.status = 'delivered'
GROUP BY c.state, c.city
ORDER BY revenue DESC;
