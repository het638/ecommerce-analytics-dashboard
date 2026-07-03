# E-Commerce Sales & Customer Analytics Dashboard

An end-to-end analytics pipeline that answers: **"Which products, cities, and customers actually drive revenue — and which customers are at risk of leaving?"**

Built with Python → MySQL → 7 SQL analytics views → Power BI + Streamlit/Plotly.

---

## Project Structure

```
ecommerce_analytics/
├── config.py                  Database connection settings (env-var driven)
├── setup.py                   Master script: creates DB, generates + loads data, builds views
├── dashboard.py                Streamlit web dashboard
├── scripts/
│   ├── generate_data.py       Generates realistic synthetic data
│   └── load_data.py           Cleans + loads data into MySQL
├── sql/
│   ├── schema.sql              Star-schema table definitions
│   └── views.sql                7 analytics views (RFM, cohorts, top products, ...)
├── data/raw/                   Generated CSVs
└── Ecommerce_Analytics_Dashboard.pbix   Power BI dashboard
```

---

## Dataset

A normalized 5-table schema, generated synthetically at realistic scale:

| Table | Rows | Contents |
|---|---|---|
| customers | 2,000 | name, email, city/state/country, registration date |
| products | 48 | 8 categories (Electronics, Clothing, Books, Sports, Home & Garden, Toys, Beauty, Food & Grocery) |
| orders | 15,000 | order date, status (delivered/cancelled/returned) |
| order_items | 44,816 | quantity, unit price, discount |
| payments | 11,879 | Credit Card, Debit Card, UPI, Net Banking, COD |

---

## How to Run

```bash
pip install pandas numpy mysql-connector-python
```
MySQL Server running locally, then set your credentials as environment variables (nothing is hardcoded):
```powershell
$env:DB_USER = "root"
$env:DB_PASSWORD = "your_password"
python setup.py    # creates DB + tables, generates data, loads it, builds views
```

Run the Streamlit dashboard:
```bash
python -m streamlit run dashboard.py
```
Or open `Ecommerce_Analytics_Dashboard.pbix` in Power BI Desktop — it connects to MySQL directly.

---

## SQL Analytics Views

| View | Purpose |
|---|---|
| `vw_monthly_revenue` | Revenue, orders, and customers per month |
| `vw_category_performance` | Revenue, units sold, and profit per product category |
| `vw_top_products` | Best-selling products ranked by revenue |
| `vw_customer_cohorts` | Customers grouped by first-purchase month, tracked over time |
| `vw_rfm` | RFM (Recency / Frequency / Monetary) customer segmentation into 7 segments — Champions, Loyal, At Risk, Lost, etc. |
| `vw_payment_methods` | Revenue and transaction breakdown by payment method |
| `vw_geo_revenue` | Revenue and orders by city/state |

---

## Key Findings

- Electronics drives **55.6%** of total revenue; Smartphone X12 is the single best-selling product.
- Delhi, Pune, and Chennai are the top 3 cities by revenue.
- "Loyal Customers" is the largest RFM segment — a healthier mix than a purely recency-driven customer base.
- No single payment method dominates (UPI, Credit Card, Debit Card, COD, Net Banking are all comparably used).

---

## Dashboards

Two front ends over the same MySQL views:

- **Streamlit** (`dashboard.py`) — dark-themed web app: KPI cards, monthly revenue trend, category donut chart, top products, RFM segments, geographic + cohort views.
- **Power BI** (`Ecommerce_Analytics_Dashboard.pbix`) — cross-filtering dashboard connected directly to MySQL via ODBC, covering the same KPIs.
