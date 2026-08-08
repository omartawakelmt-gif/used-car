"""
Used Car Market Analysis Dashboard
A comprehensive Streamlit app for exploring the used car dataset.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Used Car Market Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  – white background, premium feel
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset / base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #FFFFFF !important;
    color: #1a1a2e !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #e8eaf6;
    border-radius: 16px;
    padding: 20px 24px !important;
    box-shadow: 0 2px 16px rgba(15,52,96,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(15,52,96,0.12);
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #6c757d !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #0f3460 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.82rem !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #f8f9ff;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #e8eaf6;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 500 !important;
    color: #6c757d !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: #0f3460 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(15,52,96,0.25) !important;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1.2rem;
}
.section-header h2 {
    font-size: 1.45rem;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0;
}
.section-divider {
    height: 3px;
    background: linear-gradient(90deg, #0f3460, #e94560, transparent);
    border-radius: 2px;
    margin-bottom: 1.5rem;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 50%, #16213e 100%);
    border-radius: 20px;
    padding: 40px 50px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(233,69,96,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner h1 {
    color: #ffffff;
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 8px;
    line-height: 1.2;
}
.hero-banner p {
    color: rgba(255,255,255,0.7);
    font-size: 1.05rem;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(233,69,96,0.2);
    border: 1px solid rgba(233,69,96,0.4);
    color: #e94560;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}

/* ── Chart card ── */
.chart-card {
    background: #FFFFFF;
    border: 1px solid #e8eaf6;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(15,52,96,0.05);
}

/* ── Filter pill ── */
.filter-pill {
    background: rgba(233,69,96,0.08);
    border: 1px solid rgba(233,69,96,0.2);
    color: #e94560;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e8eaf6;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] [data-baseweb="thumb"] {
    background-color: #e94560 !important;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
VALID_FUELS = [
    "Petrol", "Diesel", "Hybrid", "LPG", "CNG",
    "Electric", "Hydrogen", "Ethanol", "Diesel Hybrid", "Other", "Unknown"
]

@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("data.csv", encoding="utf-8")

    # Keep only clean fuel-type rows
    df = df[df["fuel_type"].isin(VALID_FUELS)].copy()

    # Coerce numerics
    for col in ["year", "price_in_euro", "power_kw", "power_ps", "mileage_in_km"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fuel consumption
    df["fuel_consumption_l_100km"] = pd.to_numeric(
        df["fuel_consumption_l_100km"], errors="coerce"
    )

    # Drop extreme outliers for price and year
    df = df[df["price_in_euro"].between(500, 500_000)]
    df = df[df["year"].between(1990, 2024)]
    df = df[df["power_kw"].between(20, 1000) | df["power_kw"].isna()]
    df = df[df["mileage_in_km"].between(0, 1_500_000) | df["mileage_in_km"].isna()]

    # Capitalise brand
    df["brand"] = df["brand"].str.title()

    # Age
    df["age"] = 2024 - df["year"]

    df.reset_index(drop=True, inplace=True)
    return df


# ─────────────────────────────────────────────
#  PLOTLY THEME
# ─────────────────────────────────────────────
PALETTE = [
    "#0f3460", "#e94560", "#16213e", "#533483",
    "#2196f3", "#f59e0b", "#10b981", "#ef4444",
    "#8b5cf6", "#06b6d4", "#84cc16", "#f97316",
]
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#1a1a2e"),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#e8eaf6",
        borderwidth=1,
        font=dict(size=11),
    ),
    xaxis=dict(showgrid=True, gridcolor="#f0f0f0", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#f0f0f0", zeroline=False),
)


def styled_fig(fig, title=""):
    fig.update_layout(**CHART_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14, weight=700), x=0))
    return fig


# ─────────────────────────────────────────────
#  LOAD
# ─────────────────────────────────────────────
with st.spinner("🚗 Loading dataset…"):
    df_raw = load_data()


# ─────────────────────────────────────────────
#  SIDEBAR – FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:2.5rem;'>🚗</div>
        <div style='font-size:1.1rem; font-weight:700; color:#ffffff; margin-top:6px;'>
            Car Market<br>Dashboard
        </div>
        <div style='font-size:0.75rem; color:rgba(255,255,255,0.5); margin-top:4px;'>
            Interactive Analysis Tool
        </div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.1); margin:12px 0 20px;'>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ Filters")

    # Brand
    all_brands = sorted(df_raw["brand"].dropna().unique())
    sel_brands = st.multiselect(
        "Brand", options=all_brands,
        default=[], placeholder="All brands"
    )

    # Fuel type
    all_fuels = sorted(df_raw["fuel_type"].dropna().unique())
    sel_fuels = st.multiselect(
        "Fuel Type", options=all_fuels,
        default=[], placeholder="All fuel types"
    )

    # Transmission
    all_trans = sorted(df_raw["transmission_type"].dropna().unique())
    sel_trans = st.multiselect(
        "Transmission", options=all_trans,
        default=[], placeholder="All types"
    )

    st.markdown("---")

    # Year range
    yr_min, yr_max = int(df_raw["year"].min()), int(df_raw["year"].max())
    sel_year = st.slider("Year", yr_min, yr_max, (2005, yr_max))

    # Price range
    pr_min, pr_max = int(df_raw["price_in_euro"].min()), int(df_raw["price_in_euro"].max())
    sel_price = st.slider("Price (€)", pr_min, min(pr_max, 200_000),
                          (1_000, 80_000), step=500)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:rgba(255,255,255,0.4); text-align:center; padding:10px 0;'>
        Data: European Used Car Market<br>251 K+ listings
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FILTER DATA
# ─────────────────────────────────────────────
df = df_raw.copy()
if sel_brands:
    df = df[df["brand"].isin(sel_brands)]
if sel_fuels:
    df = df[df["fuel_type"].isin(sel_fuels)]
if sel_trans:
    df = df[df["transmission_type"].isin(sel_trans)]
df = df[df["year"].between(*sel_year)]
df = df[df["price_in_euro"].between(*sel_price)]


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🚗 European Used Car Market</div>
    <h1>Used Car Market Analysis</h1>
    <p>Explore 250K+ real listings — prices, brands, fuel types, mileage & more.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KPI METRICS
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Listings", f"{len(df):,}",
          f"{len(df)/len(df_raw)*100:.1f}% of dataset")
k2.metric("Avg Price", f"€{df['price_in_euro'].mean():,.0f}",
          f"Med: €{df['price_in_euro'].median():,.0f}")
k3.metric("Avg Mileage", f"{df['mileage_in_km'].mean():,.0f} km",
          f"Med: {df['mileage_in_km'].median():,.0f} km")
k4.metric("Avg Power", f"{df['power_kw'].mean():,.0f} kW",
          f"≈ {df['power_ps'].mean():,.0f} PS")
k5.metric("Brands", f"{df['brand'].nunique()}",
          f"{df['fuel_type'].nunique()} fuel types")

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Market Overview",
    "💰 Price Analysis",
    "🏷️ Brand Insights",
    "⚡ Performance & Fuel",
    "🔍 Data Explorer",
])


# ══════════════════════════════════════════════
#  TAB 1 – MARKET OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    # ── row 1: fuel pie + transmission donut
    c1, c2 = st.columns(2)

    with c1:
        fuel_counts = df["fuel_type"].value_counts().reset_index()
        fuel_counts.columns = ["Fuel Type", "Count"]
        fig = px.pie(
            fuel_counts, names="Fuel Type", values="Count",
            color_discrete_sequence=PALETTE,
            hole=0.45,
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig = styled_fig(fig, "Fuel Type Distribution")
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        trans_counts = df["transmission_type"].value_counts().reset_index()
        trans_counts.columns = ["Transmission", "Count"]
        fig = px.pie(
            trans_counts, names="Transmission", values="Count",
            color_discrete_sequence=PALETTE[2:],
            hole=0.45,
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig = styled_fig(fig, "Transmission Type Distribution")
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

    # ── row 2: listings by year
    year_counts = df.groupby("year").size().reset_index(name="Listings")
    fig = px.bar(
        year_counts, x="year", y="Listings",
        color="Listings",
        color_continuous_scale=["#e8eaf6", "#0f3460"],
    )
    fig.update_traces(marker_line_width=0)
    fig = styled_fig(fig, "Listings by Model Year")
    fig.update_layout(height=320, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    # ── row 3: color distribution
    if df["color"].notna().any():
        COLOR_MAP = {
            "black": "#222222", "grey": "#9e9e9e", "white": "#e0e0e0",
            "silver": "#bdbdbd", "blue": "#1565c0", "red": "#c62828",
            "brown": "#6d4c41", "green": "#2e7d32", "orange": "#e65100",
            "beige": "#d7ccc8", "yellow": "#f9a825", "bronze": "#8d6e63",
            "gold": "#f9a825", "violet": "#6a1b9a",
        }
        color_counts = (
            df["color"].dropna().value_counts().reset_index()
        )
        color_counts.columns = ["Color", "Count"]
        actual_colors = [
            COLOR_MAP.get(c.lower(), "#9e9e9e") for c in color_counts["Color"]
        ]
        fig = px.bar(
            color_counts.head(14),
            x="Color", y="Count",
            color="Color",
            color_discrete_sequence=actual_colors,
        )
        fig.update_traces(marker_line_width=0)
        fig = styled_fig(fig, "Car Color Popularity")
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 2 – PRICE ANALYSIS
# ══════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        # Price histogram
        fig = px.histogram(
            df, x="price_in_euro", nbins=80,
            color_discrete_sequence=["#0f3460"],
        )
        fig.update_traces(marker_line_width=0)
        fig = styled_fig(fig, "Price Distribution (€)")
        fig.update_layout(height=340, xaxis_tickprefix="€", xaxis_tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Price by fuel type box
        fig = px.box(
            df, x="fuel_type", y="price_in_euro",
            color="fuel_type",
            color_discrete_sequence=PALETTE,
        )
        fig = styled_fig(fig, "Price by Fuel Type (€)")
        fig.update_layout(
            height=340, showlegend=False,
            yaxis_tickprefix="€", yaxis_tickformat=","
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── price vs mileage scatter (sample for perf)
    sample = df.dropna(subset=["mileage_in_km", "price_in_euro", "fuel_type"])
    if len(sample) > 15_000:
        sample = sample.sample(15_000, random_state=42)

    fig = px.scatter(
        sample,
        x="mileage_in_km", y="price_in_euro",
        color="fuel_type",
        color_discrete_sequence=PALETTE,
        opacity=0.45,
        hover_data=["brand", "model", "year"],
    )
    fig = styled_fig(fig, "Price vs Mileage")
    fig.update_layout(
        height=380,
        xaxis_title="Mileage (km)",
        yaxis_title="Price (€)",
        xaxis_tickformat=",",
        yaxis_tickprefix="€",
        yaxis_tickformat=",",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── avg price per year line
    price_year = (
        df.groupby("year")["price_in_euro"]
        .agg(["mean", "median"])
        .reset_index()
    )
    price_year.columns = ["Year", "Mean Price", "Median Price"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price_year["Year"], y=price_year["Mean Price"],
        name="Mean", mode="lines+markers",
        line=dict(color="#0f3460", width=2.5),
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=price_year["Year"], y=price_year["Median Price"],
        name="Median", mode="lines+markers",
        line=dict(color="#e94560", width=2.5, dash="dot"),
        marker=dict(size=5),
    ))
    fig = styled_fig(fig, "Average Price by Model Year")
    fig.update_layout(
        height=320,
        yaxis_tickprefix="€",
        yaxis_tickformat=",",
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 3 – BRAND INSIGHTS
# ══════════════════════════════════════════════
with tab3:
    top_n = st.slider("Top N brands to display", 5, 30, 15, key="brand_n")

    top_brands = df["brand"].value_counts().head(top_n).reset_index()
    top_brands.columns = ["Brand", "Count"]

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            top_brands, x="Count", y="Brand",
            orientation="h",
            color="Count",
            color_continuous_scale=["#e8eaf6", "#0f3460"],
        )
        fig.update_traces(marker_line_width=0)
        fig = styled_fig(fig, f"Top {top_n} Brands by Listings")
        fig.update_layout(
            height=max(350, top_n * 24),
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        brand_price = (
            df.groupby("brand")["price_in_euro"].median()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )
        brand_price.columns = ["Brand", "Median Price"]
        fig = px.bar(
            brand_price, x="Median Price", y="Brand",
            orientation="h",
            color="Median Price",
            color_continuous_scale=["#fff3e0", "#e94560"],
        )
        fig.update_traces(marker_line_width=0)
        fig = styled_fig(fig, f"Median Price by Brand (Top {top_n})")
        fig.update_layout(
            height=max(350, top_n * 24),
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending"),
            xaxis_tickprefix="€",
            xaxis_tickformat=",",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Brand × fuel type heatmap
    st.markdown("#### 🔥 Brand × Fuel Type Heatmap")
    pivot_brands = df["brand"].value_counts().head(top_n).index.tolist()
    hm_data = (
        df[df["brand"].isin(pivot_brands)]
        .groupby(["brand", "fuel_type"])
        .size()
        .reset_index(name="count")
        .pivot(index="brand", columns="fuel_type", values="count")
        .fillna(0)
    )
    fig = px.imshow(
        hm_data,
        color_continuous_scale=["#f8f9ff", "#0f3460"],
        text_auto=True,
        aspect="auto",
    )
    fig = styled_fig(fig, "")
    fig.update_layout(height=max(350, top_n * 22))
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 4 – PERFORMANCE & FUEL
# ══════════════════════════════════════════════
with tab4:
    c1, c2 = st.columns(2)

    with c1:
        # Power distribution
        fig = px.histogram(
            df.dropna(subset=["power_kw"]),
            x="power_kw", nbins=60,
            color_discrete_sequence=["#533483"],
        )
        fig.update_traces(marker_line_width=0)
        fig = styled_fig(fig, "Engine Power Distribution (kW)")
        fig.update_layout(height=320, xaxis_title="Power (kW)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Power vs price
        samp2 = df.dropna(subset=["power_kw", "price_in_euro", "fuel_type"])
        if len(samp2) > 10_000:
            samp2 = samp2.sample(10_000, random_state=7)
        fig = px.scatter(
            samp2,
            x="power_kw", y="price_in_euro",
            color="fuel_type",
            color_discrete_sequence=PALETTE,
            opacity=0.5,
            hover_data=["brand", "model"],
        )
        fig = styled_fig(fig, "Power vs Price")
        fig.update_layout(
            height=320,
            xaxis_title="Power (kW)",
            yaxis_title="Price (€)",
            yaxis_tickprefix="€",
            yaxis_tickformat=",",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Fuel consumption
    fc_df = df.dropna(subset=["fuel_consumption_l_100km"])
    fc_df = fc_df[fc_df["fuel_consumption_l_100km"].between(2, 25)]

    c3, c4 = st.columns(2)

    with c3:
        fig = px.box(
            fc_df, x="fuel_type", y="fuel_consumption_l_100km",
            color="fuel_type",
            color_discrete_sequence=PALETTE,
        )
        fig = styled_fig(fig, "Fuel Consumption by Fuel Type (L/100km)")
        fig.update_layout(height=340, showlegend=False,
                          yaxis_title="Consumption (L/100km)")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        avg_fc = (
            fc_df.groupby("brand")["fuel_consumption_l_100km"]
            .mean()
            .sort_values()
            .head(15)
            .reset_index()
        )
        avg_fc.columns = ["Brand", "Avg Consumption"]
        fig = px.bar(
            avg_fc, x="Avg Consumption", y="Brand",
            orientation="h",
            color="Avg Consumption",
            color_continuous_scale=["#10b981", "#ef4444"],
        )
        fig.update_traces(marker_line_width=0)
        fig = styled_fig(fig, "Most Fuel-Efficient Brands (Top 15)")
        fig.update_layout(
            height=400,
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Avg L/100km",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Electric & Hybrid spotlight
    st.markdown("#### 🌿 Electric & Hybrid Market")
    eco = df[df["fuel_type"].isin(["Electric", "Hybrid", "Diesel Hybrid", "Hydrogen"])]
    if len(eco) > 0:
        c5, c6 = st.columns(2)
        with c5:
            eco_brand = eco["brand"].value_counts().head(15).reset_index()
            eco_brand.columns = ["Brand", "Count"]
            fig = px.bar(
                eco_brand, x="Count", y="Brand",
                orientation="h",
                color="Count",
                color_continuous_scale=["#e8f5e9", "#10b981"],
            )
            fig.update_traces(marker_line_width=0)
            fig = styled_fig(fig, "Top Eco Brands")
            fig.update_layout(
                height=380,
                coloraxis_showscale=False,
                yaxis=dict(categoryorder="total ascending"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with c6:
            eco_year = eco.groupby(["year", "fuel_type"]).size().reset_index(name="Count")
            fig = px.line(
                eco_year, x="year", y="Count",
                color="fuel_type",
                color_discrete_sequence=["#10b981", "#2196f3", "#533483", "#06b6d4"],
                markers=True,
            )
            fig = styled_fig(fig, "Eco Car Listings by Year")
            fig.update_layout(height=380, xaxis_title="Year", yaxis_title="Listings")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Electric/Hybrid cars match current filters.")


# ══════════════════════════════════════════════
#  TAB 5 – DATA EXPLORER
# ══════════════════════════════════════════════
with tab5:
    st.markdown("#### 🔍 Filter & Explore Raw Data")

    col_opts = [
        "brand", "model", "color", "year", "price_in_euro",
        "power_kw", "power_ps", "transmission_type",
        "fuel_type", "fuel_consumption_l_100km",
        "mileage_in_km", "offer_description",
    ]
    visible_cols = st.multiselect(
        "Columns to display", options=col_opts,
        default=["brand", "model", "year", "price_in_euro",
                 "fuel_type", "transmission_type", "mileage_in_km"],
    )

    sort_col = st.selectbox("Sort by", options=visible_cols,
                            index=visible_cols.index("price_in_euro")
                            if "price_in_euro" in visible_cols else 0)
    sort_asc = st.radio("Sort order", ["Ascending", "Descending"],
                        horizontal=True) == "Ascending"

    page_size = st.slider("Rows per page", 10, 200, 50, key="page_size")

    display_df = (
        df[visible_cols]
        .sort_values(sort_col, ascending=sort_asc)
        .reset_index(drop=True)
    )

    st.markdown(f"**{len(display_df):,} listings** match your filters.")
    st.dataframe(
        display_df.head(page_size),
        use_container_width=True,
        height=480,
    )

    # Download
    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv_data,
        file_name="used_cars_filtered.csv",
        mime="text/csv",
    )

    # Summary stats
    st.markdown("#### 📐 Summary Statistics")
    num_cols = [c for c in visible_cols
                if c in ["price_in_euro", "power_kw", "mileage_in_km",
                         "fuel_consumption_l_100km", "year", "power_ps"]]
    if num_cols:
        st.dataframe(
            df[num_cols].describe().round(2),
            use_container_width=True,
        )
