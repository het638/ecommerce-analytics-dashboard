import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from config import DB_CONFIG

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding: 1.5rem 2rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252840);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid;
        margin-bottom: 0.5rem;
    }
    .card-blue  { border-color: #4f8ef7; }
    .card-green { border-color: #2ecc71; }
    .card-orange{ border-color: #f39c12; }
    .card-purple{ border-color: #9b59b6; }
    .metric-label { color: #8b95a5; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { color: #ffffff; font-size: 2rem; font-weight: 700; margin-top: 0.2rem; }
    .metric-delta { font-size: 0.8rem; margin-top: 0.1rem; }
    .section-title {
        color: #e0e6f0;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #2a2d3e;
    }
    .stPlotlyChart { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

CHART_THEME = dict(
    paper_bgcolor="#1e2130",
    plot_bgcolor="#1e2130",
    font=dict(color="#c0c8d8", family="Inter, sans-serif"),
    margin=dict(t=40, b=30, l=30, r=20),
)

COLORS = ["#4f8ef7","#2ecc71","#f39c12","#9b59b6","#e74c3c","#1abc9c","#e67e22","#3498db"]

@st.cache_data(ttl=300)
def query(sql):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# ── Load data ─────────────────────────────────────────────────
rev   = query("SELECT * FROM vw_monthly_revenue ORDER BY month")
cat   = query("SELECT * FROM vw_category_performance")
top   = query("SELECT * FROM vw_top_products LIMIT 10")
rfm   = query("SELECT segment, COUNT(*) as customers, ROUND(SUM(monetary),2) as revenue FROM vw_rfm GROUP BY segment ORDER BY customers DESC")
geo   = query("SELECT * FROM vw_geo_revenue LIMIT 10")
pay   = query("SELECT * FROM vw_payment_methods")
cohort= query("SELECT cohort_month, SUM(cohort_revenue) as revenue, SUM(active_customers) as customers FROM vw_customer_cohorts GROUP BY cohort_month ORDER BY cohort_month")

# ── Header ────────────────────────────────────────────────────
st.markdown("## 🛒 E-Commerce Sales & Customer Analytics")
st.markdown("<p style='color:#8b95a5;margin-top:-0.8rem;'>Real-time dashboard powered by MySQL</p>", unsafe_allow_html=True)
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────
total_rev    = rev["gross_revenue"].sum()
total_orders = rev["total_orders"].sum()
total_cust   = query("SELECT COUNT(*) as n FROM customers")["n"][0]
avg_order    = rev["avg_order_value"].mean()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card card-blue">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">₹{total_rev:,.0f}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card card-green">
        <div class="metric-label">Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card card-orange">
        <div class="metric-label">Total Customers</div>
        <div class="metric-value">{total_cust:,}</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="metric-card card-purple">
        <div class="metric-label">Avg Order Value</div>
        <div class="metric-value">₹{avg_order:,.0f}</div>
    </div>""", unsafe_allow_html=True)

# ── Row 1: Revenue Trend + Category ───────────────────────────
st.markdown('<div class="section-title">Revenue & Category Performance</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rev["month"], y=rev["gross_revenue"],
        mode="lines+markers",
        line=dict(color="#4f8ef7", width=3),
        marker=dict(size=6, color="#4f8ef7"),
        fill="tozeroy", fillcolor="rgba(79,142,247,0.08)",
        name="Revenue"
    ))
    fig.add_trace(go.Bar(
        x=rev["month"], y=rev["total_orders"],
        name="Orders", yaxis="y2",
        marker_color="rgba(46,204,113,0.4)",
    ))
    fig.update_layout(
        **CHART_THEME,
        title="Monthly Revenue & Orders",
        yaxis=dict(title="Revenue (₹)", gridcolor="#2a2d3e", color="#8b95a5"),
        yaxis2=dict(title="Orders", overlaying="y", side="right", color="#8b95a5"),
        legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.pie(
        cat, values="revenue", names="category",
        color_discrete_sequence=COLORS,
        hole=0.55,
        title="Revenue by Category",
    )
    fig2.update_traces(textposition="outside", textinfo="label+percent")
    fig2.update_layout(**CHART_THEME, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Top Products + Payment Methods ─────────────────────
st.markdown('<div class="section-title">Top Products & Payment Methods</div>', unsafe_allow_html=True)
col3, col4 = st.columns([2, 1])

with col3:
    fig3 = px.bar(
        top.sort_values("revenue"), x="revenue", y="product_name",
        orientation="h", color="category",
        color_discrete_sequence=COLORS,
        title="Top 10 Products by Revenue",
        labels={"revenue": "Revenue (₹)", "product_name": ""},
    )
    fig3.update_layout(**CHART_THEME, yaxis=dict(gridcolor="#2a2d3e"), xaxis=dict(gridcolor="#2a2d3e"))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.bar(
        pay, x="total_amount", y="method",
        orientation="h", color="method",
        color_discrete_sequence=COLORS,
        title="Payment Methods",
        labels={"total_amount": "Revenue (₹)", "method": ""},
    )
    fig4.update_layout(**CHART_THEME, showlegend=False, yaxis=dict(gridcolor="#2a2d3e"), xaxis=dict(gridcolor="#2a2d3e"))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: RFM Segments + Geo ─────────────────────────────────
st.markdown('<div class="section-title">Customer Segmentation & Geography</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    fig5 = px.bar(
        rfm, x="segment", y="customers",
        color="segment", color_discrete_sequence=COLORS,
        title="RFM Customer Segments",
        labels={"customers": "Customers", "segment": ""},
        text="customers",
    )
    fig5.update_traces(textposition="outside")
    fig5.update_layout(**CHART_THEME, showlegend=False, xaxis=dict(gridcolor="#2a2d3e"), yaxis=dict(gridcolor="#2a2d3e"))
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.bar(
        geo.sort_values("revenue", ascending=False).head(10),
        x="city", y="revenue",
        color="state", color_discrete_sequence=COLORS,
        title="Top 10 Cities by Revenue",
        labels={"revenue": "Revenue (₹)", "city": ""},
    )
    fig6.update_layout(**CHART_THEME, xaxis=dict(gridcolor="#2a2d3e"), yaxis=dict(gridcolor="#2a2d3e"))
    st.plotly_chart(fig6, use_container_width=True)

# ── Row 4: Cohort ─────────────────────────────────────────────
st.markdown('<div class="section-title">Customer Cohort Revenue Over Time</div>', unsafe_allow_html=True)
fig7 = go.Figure()
fig7.add_trace(go.Bar(
    x=cohort["cohort_month"], y=cohort["revenue"],
    marker=dict(color=cohort["revenue"], colorscale="Blues"),
    name="Cohort Revenue"
))
fig7.update_layout(
    **CHART_THEME,
    title="Revenue by Customer Acquisition Cohort",
    xaxis=dict(gridcolor="#2a2d3e", color="#8b95a5"),
    yaxis=dict(gridcolor="#2a2d3e", color="#8b95a5", title="Revenue (₹)"),
)
st.plotly_chart(fig7, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.markdown("<p style='text-align:center;color:#3a3f55;font-size:0.8rem;'>E-Commerce Analytics Dashboard • Python + MySQL + Streamlit</p>", unsafe_allow_html=True)
