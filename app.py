import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as graph_objects
from datetime import datetime, timedelta
import os
import sys
import numpy as np

# Ensure src/ is in the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from etl_pipeline import run_etl
from data_generator import generate_marketing_data
from ai_assistant import (
    analyze_campaign_performance,
    recommend_budget_reallocations,
    generate_weekly_report,
    answer_business_question,
    HAS_GEMINI
)

# ------------------
# Page Configuration
# ------------------
st.set_page_config(
    page_title="AdVantage AI // Cyber-Intelligence Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------
# Next-Gen Ultra-Premium CSS Theme
# ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --bg-dark: #040711;
        --card-bg: rgba(13, 20, 36, 0.75);
        --accent-cyan: #00f2fe;
        --accent-purple: #7928ca;
        --accent-pink: #ff0080;
        --accent-green: #10b981;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: var(--bg-dark);
        color: #f8fafc;
    }
    
    h1, h2, h3, .brand-title {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Custom Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070c1a 0%, #03060d 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #38bdf8 !important;
        border-left: 3px solid #00f2fe;
        padding-left: 10px;
        margin-top: 15px;
    }
    
    /* Multiselect Tags Styling */
    div[data-baseweb="tag"] {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.2) 0%, rgba(121, 40, 202, 0.3) 100%) !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="tag"] span {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    /* Custom Styled Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #030712 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(0, 242, 254, 0.5) !important;
        color: #000000 !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    
    button[data-baseweb="tab"]:hover {
        color: #00f2fe !important;
        background: rgba(255, 255, 255, 0.03) !important;
    }
    
    button[aria-selected="true"] {
        color: #00f2fe !important;
        border-bottom: 3px solid #00f2fe !important;
        background: rgba(0, 242, 254, 0.05) !important;
    }

    /* Top Cyber Status Bar */
    .top-status-bar {
        background: linear-gradient(90deg, rgba(13, 20, 36, 0.95) 0%, rgba(24, 15, 42, 0.95) 50%, rgba(13, 20, 36, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.25);
        padding: 12px 24px;
        border-radius: 16px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.12);
        backdrop-filter: blur(12px);
    }
    
    .status-pulse {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 12px #10b981;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    .ticker-stat {
        font-size: 0.88rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    .ticker-stat strong {
        color: #f8fafc;
        font-weight: 700;
    }

    /* Hero Banner */
    .hero-glow-card {
        background: radial-gradient(circle at 85% 15%, rgba(121, 40, 202, 0.3) 0%, transparent 45%),
                    radial-gradient(circle at 15% 85%, rgba(0, 242, 254, 0.25) 0%, transparent 50%),
                    linear-gradient(135deg, #0b0f1a 0%, #111827 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 3rem;
        margin-bottom: 2.5rem;
        position: relative;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
        overflow: hidden;
    }
    
    .hero-glow-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #00f2fe, #7928ca, #ff0080, #00f2fe);
    }
    
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 242, 254, 0.12);
        border: 1px solid rgba(0, 242, 254, 0.35);
        color: #38bdf8;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 1rem;
    }

    .hero-main-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0 0 1rem 0;
        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px;
    }
    
    .hero-subtext {
        font-size: 1.15rem;
        color: #94a3b8;
        max-width: 840px;
        line-height: 1.6;
    }

    /* Cyber Metric Cards */
    .cyber-metric-card {
        background: rgba(13, 20, 36, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .cyber-metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 242, 254, 0.45);
        box-shadow: 0 15px 35px rgba(0, 242, 254, 0.2);
    }
    
    .card-icon-badge {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        margin-bottom: 12px;
    }
    
    .badge-cyan { background: rgba(0, 242, 254, 0.15); color: #00f2fe; border: 1px solid rgba(0, 242, 254, 0.35); }
    .badge-purple { background: rgba(121, 40, 202, 0.15); color: #c084fc; border: 1px solid rgba(121, 40, 202, 0.35); }
    .badge-pink { background: rgba(255, 0, 128, 0.15); color: #ff0080; border: 1px solid rgba(255, 0, 128, 0.35); }
    .badge-green { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.35); }

    .card-label {
        font-size: 0.8rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .card-main-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 4px 0;
    }
    
    .card-trend-badge {
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 6px;
    }
    
    .trend-up { background: rgba(16, 185, 129, 0.15); color: #34d399; }
    .trend-down { background: rgba(239, 68, 68, 0.15); color: #f87171; }

    /* Custom AI Chat Box */
    .ai-response-box {
        background: linear-gradient(135deg, rgba(13, 20, 36, 0.95) 0%, rgba(24, 32, 54, 0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
        margin-top: 1rem;
        color: #e2e8f0;
    }

    .user-question-box {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        color: #f1f5f9;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Connection helper
def get_db_connection():
    db_path = "data/marketing.db"
    if not os.path.exists(db_path):
        run_etl()
    return sqlite3.connect(db_path)

# Load data
conn = get_db_connection()
df_campaigns = pd.read_sql_query("""
    SELECT p.*, c.Campaign_Name, c.Platform, c.Campaign_Type 
    FROM fact_daily_ad_performance p
    JOIN dim_campaigns c ON p.Campaign_ID = c.Campaign_ID
""", conn)
df_campaigns["Date"] = pd.to_datetime(df_campaigns["Date"])

df_web = pd.read_sql_query("SELECT * FROM fact_daily_website_performance", conn)
df_web["Date"] = pd.to_datetime(df_web["Date"])
conn.close()

# Ticker stats
total_ad_spend = df_campaigns["Spend"].sum()
total_ad_revenue = df_campaigns["Revenue"].sum()
blended_roas = total_ad_revenue / total_ad_spend
all_loaded_brands = sorted(list(df_campaigns["Brand_Name"].unique()))

# ------------------
# Top Cyber Status Ticker
# ------------------
st.markdown(f"""
<div class="top-status-bar">
    <div style="display: flex; align-items: center;">
        <span class="status-pulse"></span>
        <span class="ticker-stat">SYSTEM STATUS: <strong>LIVE ATTRITION ENGINE</strong></span>
    </div>
    <div class="ticker-stat">WAREHOUSE CAPACITY: <strong>{len(all_loaded_brands)} BRANDS INGESTED</strong></div>
    <div class="ticker-stat">NETWORK REVENUE: <strong style="color: #10b981;">${total_ad_revenue:,.2f}</strong></div>
    <div class="ticker-stat">BLENDED ROAS: <strong style="color: #38bdf8;">{blended_roas:.2f}x ▲</strong></div>
</div>
""", unsafe_allow_html=True)

# ------------------
# Hero Banner
# ------------------
st.markdown("""
<div class="hero-glow-card">
    <div class="hero-tag">⚡ AI Growth & Attribution Intelligence</div>
    <h1 class="hero-main-title">AdVantage AI Engine</h1>
    <p class="hero-subtext">
        Multi-brand performance intelligence suite. Audit campaign performance, run predictive scenario simulations, execute natural language SQL queries, and inspect growth metrics across 30+ top D2C & global brands including Minimalist, Nykaa, Gymshark, Nike, and Apple.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------
# Sidebar Configuration
# ------------------
st.sidebar.markdown("### 🏷️ Brand Selector")

default_selection = ["Minimalist", "Nykaa", "Mamaearth", "Gymshark", "Nike", "Apple"]
valid_defaults = [b for b in default_selection if b in all_loaded_brands]

selected_brands = st.sidebar.multiselect(
    "Select Active Brands",
    options=all_loaded_brands,
    default=valid_defaults if valid_defaults else all_loaded_brands[:5]
)

# On-the-fly Custom Brand Creator
with st.sidebar.expander("➕ Generate Custom Brand"):
    st.write("Synthesize ad metrics for any custom brand:")
    new_brand_name = st.text_input("Brand Name", placeholder="e.g. Tesla, Glossier, Puma")
    new_brand_cat = st.selectbox("Category", ["Consumer Electronics", "Apparel & Fashion", "Beauty & Skincare", "Automotive", "Luxury Goods", "Other"])
    
    if st.button("🚀 Add Brand to Warehouse"):
        if new_brand_name and new_brand_name not in all_loaded_brands:
            with st.spinner(f"Synthesizing 365-day dataset for '{new_brand_name}'..."):
                from data_generator import BUILTIN_BRANDS
                custom_brand_dict = {"name": new_brand_name, "category": new_brand_cat, "spend_mult": np.random.uniform(0.8, 1.4), "roas_target": 3.0}
                all_brand_dicts = BUILTIN_BRANDS + [custom_brand_dict]
                generate_marketing_data(all_brand_dicts)
                run_etl()
                st.sidebar.success(f"Added {new_brand_name} to database!")
                st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Filter Controls")

min_date = df_campaigns["Date"].min().to_pydatetime()
max_date = df_campaigns["Date"].max().to_pydatetime()

start_date, end_date = st.sidebar.slider(
    "Date Window",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

platforms = df_campaigns["Platform"].unique()
selected_platforms = st.sidebar.multiselect(
    "Attribution Channels",
    options=platforms,
    default=list(platforms)
)

campaign_types = df_campaigns["Campaign_Type"].unique()
selected_types = st.sidebar.multiselect(
    "Funnel Stage",
    options=campaign_types,
    default=list(campaign_types)
)

if st.sidebar.button("⚡ Force Re-run Pipeline (ETL)"):
    with st.spinner("Processing multi-brand data pipelines..."):
        run_etl()
        st.sidebar.success("Database regenerated!")
        st.rerun()

# Apply Filters
df_filtered_camp = df_campaigns[
    (df_campaigns["Brand_Name"].isin(selected_brands)) &
    (df_campaigns["Date"] >= start_date) &
    (df_campaigns["Date"] <= end_date) &
    (df_campaigns["Platform"].isin(selected_platforms)) &
    (df_campaigns["Campaign_Type"].isin(selected_types))
]

df_filtered_web = df_web[
    (df_web["Brand_Name"].isin(selected_brands)) &
    (df_web["Date"] >= start_date) &
    (df_web["Date"] <= end_date)
]

# ------------------
# Navigation Tabs
# ------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Dashboard",
    "🏷️ Brand Benchmarks & Deep Dive",
    "🔮 Scenario & Forecast Planner",
    "🤖 Cognitive AI Audits",
    "💬 Interactive AI Analyst",
    "🧪 Data Warehouse & SQL Sandbox"
])

# ==========================================
# TAB 1: EXECUTIVE DASHBOARD
# ==========================================
with tab1:
    spend_val = df_filtered_camp["Spend"].sum()
    revenue_val = df_filtered_camp["Revenue"].sum()
    roas_val = revenue_val / spend_val if spend_val > 0 else 0
    purchases_val = df_filtered_camp["Purchases"].sum()
    cac_val = spend_val / purchases_val if purchases_val > 0 else 0
    
    web_sessions_val = df_filtered_web["Sessions"].sum()
    web_conversions_val = df_filtered_web["Conversions"].sum()
    cr_val = (web_conversions_val / web_sessions_val) * 100 if web_sessions_val > 0 else 0
    
    # Futuristic Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        st.markdown(f"""
        <div class="cyber-metric-card">
            <div class="card-icon-badge badge-cyan">💰</div>
            <div class="card-label">Attributed Revenue</div>
            <div class="card-main-val">${revenue_val:,.0f}</div>
            <div class="card-trend-badge trend-up">⚡ High Value Target</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="cyber-metric-card">
            <div class="card-icon-badge badge-purple">🎯</div>
            <div class="card-label">Total Ad Spend</div>
            <div class="card-main-val">${spend_val:,.0f}</div>
            <div class="card-trend-badge trend-down">Meta + Google</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="cyber-metric-card">
            <div class="card-icon-badge badge-pink">🚀</div>
            <div class="card-label">Blended ROAS</div>
            <div class="card-main-val" style="color: #c084fc;">{roas_val:.2f}x</div>
            <div class="card-trend-badge trend-up">Target: > 3.0x</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="cyber-metric-card">
            <div class="card-icon-badge badge-cyan">👤</div>
            <div class="card-label">Blended CAC</div>
            <div class="card-main-val" style="color: #38bdf8;">${cac_val:.2f}</div>
            <div class="card-trend-badge trend-up">Avg Order: ~$80</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="cyber-metric-card">
            <div class="card-icon-badge badge-green">📈</div>
            <div class="card-label">Web Conv Rate</div>
            <div class="card-main-val" style="color: #34d399;">{cr_val:.2f}%</div>
            <div class="card-trend-badge trend-up">Traffic to Sales</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        df_daily_agg = df_filtered_camp.groupby("Date")[["Spend", "Revenue"]].sum().reset_index()
        fig_trend = graph_objects.Figure()
        
        fig_trend.add_trace(graph_objects.Scatter(
            x=df_daily_agg["Date"], y=df_daily_agg["Revenue"],
            name="Revenue Generated", mode="lines", fill="tozeroy",
            line=dict(color="#00f2fe", width=3),
            fillcolor="rgba(0, 242, 254, 0.12)"
        ))
        
        fig_trend.add_trace(graph_objects.Scatter(
            x=df_daily_agg["Date"], y=df_daily_agg["Spend"],
            name="Ad Spend", mode="lines",
            line=dict(color="#ff0080", width=2.5, dash="dash")
        ))
        
        fig_trend.update_layout(
            title=dict(text="Revenue vs Spend Daily Timeline", font=dict(family="Space Grotesk", size=18, color="#ffffff")),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        df_brand_revenue = df_filtered_camp.groupby("Brand_Name")["Revenue"].sum().reset_index()
        fig_pie = px.pie(
            df_brand_revenue, values="Revenue", names="Brand_Name",
            title="Revenue Contribution by Selected Brands",
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Turbo
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=dict(font=dict(family="Space Grotesk", size=16))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    col_l2, col_r2 = st.columns(2)
    
    with col_l2:
        df_bubble = df_filtered_camp.groupby(["Campaign_Name", "Platform"]).agg({
            "Spend": "sum",
            "Revenue": "sum",
            "Purchases": "sum",
            "Clicks": "sum"
        }).reset_index()
        df_bubble["ROAS"] = df_bubble["Revenue"] / df_bubble["Spend"]
        
        fig_bubble = px.scatter(
            df_bubble, x="Spend", y="ROAS",
            size="Purchases", color="Platform",
            hover_name="Campaign_Name", size_max=45,
            title="Campaign Efficiency Matrix (ROAS vs Spend vs Purchases)",
            color_discrete_map={"Google Ads": "#00f2fe", "Meta Ads": "#ff0080"}
        )
        fig_bubble.add_hline(y=3.0, line_dash="dash", line_color="#10b981", annotation_text="Target ROAS (3x)")
        fig_bubble.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=dict(font=dict(family="Space Grotesk", size=16))
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    with col_r2:
        df_chan_agg = df_filtered_web.groupby("Channel")["Sessions"].sum().reset_index()
        fig_bar = px.bar(
            df_chan_agg, x="Channel", y="Sessions",
            color="Channel",
            title="Traffic Breakdown by Acquisition Channel",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=dict(font=dict(family="Space Grotesk", size=16))
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# TAB 2: BRAND BENCHMARKS & DEEP DIVE
# ==========================================
with tab2:
    st.subheader("🏷️ Brand Benchmarks & Performance Leaderboard")
    st.write("Compare growth metrics across all brands loaded in your warehouse.")
    
    df_brand_summary = df_filtered_camp.groupby("Brand_Name").agg({
        "Spend": "sum",
        "Revenue": "sum",
        "Purchases": "sum",
        "Clicks": "sum",
        "Impressions": "sum"
    }).reset_index()
    
    df_brand_summary["ROAS"] = df_brand_summary["Revenue"] / df_brand_summary["Spend"]
    df_brand_summary["CAC"] = df_brand_summary["Spend"] / df_brand_summary["Purchases"]
    df_brand_summary["CTR (%)"] = (df_brand_summary["Clicks"] / df_brand_summary["Impressions"]) * 100
    df_brand_summary["CPC ($)"] = df_brand_summary["Spend"] / df_brand_summary["Clicks"]
    
    # Leaderboard Table
    st.dataframe(
        df_brand_summary.sort_values(by="ROAS", ascending=False).style.format({
            "Spend": "${:,.2f}", "Revenue": "${:,.2f}", "ROAS": "{:.2f}x", "CAC": "${:.2f}", "CTR (%)": "{:.2f}%", "CPC ($)": "${:.2f}"
        }),
        use_container_width=True
    )
    
    st.markdown("---")
    
    cb1, cb2 = st.columns(2)
    
    with cb1:
        fig_b_roas = px.bar(
            df_brand_summary.sort_values(by="ROAS", ascending=False), x="Brand_Name", y="ROAS",
            color="ROAS",
            title="ROAS Leaderboard across Selected Brands",
            color_continuous_scale="Viridis"
        )
        fig_b_roas.add_hline(y=3.0, line_dash="dash", line_color="#10b981", annotation_text="Benchmark (3x)")
        fig_b_roas.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=dict(font=dict(family="Space Grotesk", size=16))
        )
        st.plotly_chart(fig_b_roas, use_container_width=True)
        
    with cb2:
        fig_b_cac = px.bar(
            df_brand_summary.sort_values(by="CAC"), x="Brand_Name", y="CAC",
            color="CAC",
            title="Customer Acquisition Cost (CAC) by Brand (Lower is Better)",
            color_continuous_scale="Magma"
        )
        fig_b_cac.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=dict(font=dict(family="Space Grotesk", size=16))
        )
        st.plotly_chart(fig_b_cac, use_container_width=True)

    st.markdown("---")
    st.subheader("🔍 Single Brand Deep Inspection")
    target_brand = st.selectbox("Select Any Brand for Deep Inspection:", all_loaded_brands, index=all_loaded_brands.index("Minimalist") if "Minimalist" in all_loaded_brands else 0)
    
    df_single_brand = df_campaigns[df_campaigns["Brand_Name"] == target_brand]
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.write(f"#### Top Campaigns for **{target_brand}**")
        df_sb_camps = df_single_brand.groupby("Campaign_Name").agg({
            "Spend": "sum",
            "Revenue": "sum",
            "Purchases": "sum"
        }).reset_index()
        df_sb_camps["ROAS"] = df_sb_camps["Revenue"] / df_sb_camps["Spend"]
        df_sb_camps = df_sb_camps.sort_values(by="ROAS", ascending=False)
        st.dataframe(df_sb_camps.style.format({"Spend": "${:,.2f}", "Revenue": "${:,.2f}", "ROAS": "{:.2f}x"}), use_container_width=True)
        
    with col_sb2:
        st.write(f"#### Spend Allocation for **{target_brand}**")
        fig_sb_pie = px.pie(
            df_sb_camps, values="Spend", names="Campaign_Name",
            title=f"Campaign Spend Breakdown for {target_brand}",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Sunset
        )
        fig_sb_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_sb_pie, use_container_width=True)

# ==========================================
# TAB 3: SCENARIO & FORECAST PLANNER
# ==========================================
with tab3:
    st.subheader("🔮 Predictive Budget & ROAS Forecaster")
    st.markdown("Use this scenario planner to model revenue variation when reallocating Google vs Meta ad budgets.")
    
    col_s1, col_s2 = st.columns([1, 2])
    
    with col_s1:
        st.write("### Model Controls")
        sim_google_budget = st.slider("Google Ads Daily Budget ($)", 500, 20000, 5000, 500)
        sim_meta_budget = st.slider("Meta Ads Daily Budget ($)", 500, 20000, 4000, 500)
        conversion_optimism = st.slider("Market Conversion Factor", 0.5, 2.0, 1.0, 0.1)
        
    with col_s2:
        est_google_rev = sim_google_budget * 2.8 * (1.0 + np.log10(sim_google_budget/1000.0) * -0.2) * conversion_optimism
        est_meta_rev = sim_meta_budget * 2.9 * (1.0 + np.log10(sim_meta_budget/650.0) * -0.15) * conversion_optimism
        
        est_total_spend = sim_google_budget + sim_meta_budget
        est_total_revenue = est_google_rev + est_meta_rev
        est_blended_roas = est_total_revenue / est_total_spend
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric("Simulated Monthly Spend", f"${est_total_spend * 30:,.2f}", "+30 Days")
        with sc2:
            st.metric("Forecasted Monthly Revenue", f"${est_total_revenue * 30:,.2f}", f"{est_blended_roas:.2f}x ROAS")
        with sc3:
            st.metric("Estimated Purchases", f"{int(est_total_revenue / 85 * 30):,}", "Assuming $85 AOV")
            
        fig_sim = graph_objects.Figure()
        fig_sim.add_trace(graph_objects.Bar(
            x=["Current Baseline (Actuals)", "Simulated Projection"],
            y=[total_ad_revenue, est_total_revenue * 365],
            marker_color=["#334155", "#00f2fe"],
            width=[0.4, 0.4]
        ))
        fig_sim.update_layout(
            title=dict(text="12-Month Projected Value Comparison", font=dict(family="Space Grotesk", size=16)),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_sim, use_container_width=True)

# ==========================================
# TAB 4: COGNITIVE AI AUDITS
# ==========================================
with tab4:
    st.subheader("🧠 Deep Cognitive Auditing (Gemini AI)")
    
    c_audit, c_budget = st.columns(2)
    
    with c_audit:
        st.markdown("### 📊 Performance Auditing Engine")
        if st.button("Initialize Portfolio Audit"):
            with st.spinner("AI is analyzing selected brand campaigns..."):
                res = analyze_campaign_performance(df_filtered_camp)
                st.markdown(f"<div class=\"ai-response-box\">{res}</div>", unsafe_allow_html=True)
                
    with c_budget:
        st.markdown("### 💸 Reallocation AI Suggestions")
        if st.button("Generate Reallocation Model"):
            with st.spinner("Rebalancing ad budgets..."):
                res = recommend_budget_reallocations(df_filtered_camp)
                st.markdown(f"<div class=\"ai-response-box\">{res}</div>", unsafe_allow_html=True)
                
    st.markdown("---")
    st.write("### 📅 Export Automated Executive Briefing")
    if st.button("Compile Executive Briefing"):
        with st.spinner("Compiling report..."):
            res = generate_weekly_report(df_filtered_camp, df_filtered_web)
            st.markdown(f"<div class=\"ai-response-box\">{res}</div>", unsafe_allow_html=True)

# ==========================================
# TAB 5: INTERACTIVE AI ANALYST
# ==========================================
with tab5:
    st.subheader("💬 Conversations with AdVantage AI Analyst")
    st.write("Query the SQLite data warehouse directly using natural business language.")
    
    user_query = st.text_input("Ask a marketing question:", placeholder="Which brand has the highest overall ROAS?")
    
    if st.button("Process Question"):
        if user_query:
            st.markdown(f"<div class=\"user-question-box\">🧑‍💼 <b>You:</b> {user_query}</div>", unsafe_allow_html=True)
            with st.spinner("Executing SQL query across brand database..."):
                res = answer_business_question(user_query)
                st.markdown(f"<div class=\"ai-response-box\">{res}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

# ==========================================
# TAB 6: DATA WAREHOUSE & SQL SANDBOX
# ==========================================
with tab6:
    st.subheader("🧪 SQLite Data Warehouse Inspector")
    
    selected_tbl = st.selectbox(
        "Choose warehouse table to audit:",
        ["dim_campaigns", "fact_daily_ad_performance", "fact_daily_website_performance", "raw_google_ads", "raw_meta_ads", "raw_website_analytics"]
    )
    
    conn = get_db_connection()
    df_tbl = pd.read_sql_query(f"SELECT * FROM {selected_tbl} LIMIT 50", conn)
    conn.close()
    
    st.write(f"Showing first 50 rows of `{selected_tbl}`:")
    st.dataframe(df_tbl, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💻 Developer Sandbox (SQL)")
    
    sql_sandbox_input = st.text_area("Write SQL Query:", "SELECT Brand_Name, Platform, SUM(Spend) AS Spend, SUM(Revenue) AS Revenue, SUM(Revenue)/SUM(Spend) AS ROAS FROM fact_daily_ad_performance p JOIN dim_campaigns c ON p.Campaign_ID = c.Campaign_ID GROUP BY Brand_Name, Platform;")
    
    if st.button("Execute Raw SQL Query"):
        if sql_sandbox_input:
            try:
                conn = get_db_connection()
                df_sql_res = pd.read_sql_query(sql_sandbox_input, conn)
                conn.close()
                st.success("Query compiled and executed successfully!")
                st.dataframe(df_sql_res, use_container_width=True)
                
                csv = df_sql_res.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download results as CSV",
                    data=csv,
                    file_name="brand_sandbox_query_results.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"SQL Compiler Error: {str(e)}")
