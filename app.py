import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------------------------------------
# 1. Page Configuration & Dark Obsidian Theme Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Adidas Executive Commercial Intelligence",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        /* Base page background */
        .stApp {
            background-color: #0A0A0C;
            color: #E2E8F0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Reduce top padding */
        .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 2rem !important;
        }

        /* Top Header Styling */
        .header-title {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: #FFFFFF;
            margin-bottom: 2px;
        }
        .header-subtitle {
            font-size: 0.90rem;
            font-weight: 400;
            color: #64748B;
            margin-bottom: 12px;
        }

        /* Custom KPI Card Containers */
        .kpi-card {
            background-color: #14161D;
            border: 1px solid #232733;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            margin-bottom: 12px;
        }
        .kpi-title {
            font-size: 0.80rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94A3B8;
            margin-bottom: 4px;
        }
        .kpi-value {
            font-size: 2.0rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.03em;
            margin-bottom: 4px;
        }
        .kpi-delta {
            font-size: 0.80rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .delta-positive { color: #10B981; }
        .delta-negative { color: #EF4444; }

        /* Regional micro-table */
        .region-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 7px 0;
            border-bottom: 1px solid #1E222D;
            font-size: 0.83rem;
        }
        .region-name { color: #CBD5E1; font-weight: 500; }
        .region-val { color: #FFFFFF; font-weight: 700; }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0D0E12;
            border-right: 1px solid #1E222D;
        }
        .sidebar-brand {
            font-size: 1.4rem;
            font-weight: 900;
            letter-spacing: 0.15em;
            color: #FFFFFF;
            margin-top: 6px;
            margin-bottom: 4px;
        }
        .sidebar-slogan {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.2em;
            color: #64748B;
            text-transform: uppercase;
            margin-bottom: 25px;
        }

        label {
            color: #94A3B8 !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. Data Loading & Feature Pipeline
# ---------------------------------------------------------
US_STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

@st.cache_data
def load_data():
    df = pd.read_csv("Adidas US Sales.csv")
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["year"] = df["invoice_date"].dt.year
    df["month_num"] = df["invoice_date"].dt.month
    df["month_name"] = df["invoice_date"].dt.strftime("%b")
    df["category"] = df["product"].apply(
        lambda x: "Footwear" if "Footwear" in x else ("Apparel" if "Apparel" in x else "Accessories")
    )
    df["state_code"] = df["state"].map(US_STATE_ABBREV)
    return df

raw_df = load_data()

# ---------------------------------------------------------
# 3. Sidebar Navigation & Branding
# ---------------------------------------------------------
ADIDAS_WHITE_LOGO_SVG = """
<svg fill="#FFFFFF" width="68" height="46" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 8px;">
    <path d="m24 19.535-8.697-15.07-4.659 2.687 7.145 12.383Zm-8.287 0L9.969 9.59 5.31 12.277l4.192 7.258ZM4.658 14.723l2.776 4.812H1.223L0 17.41Z"/>
</svg>
"""

with st.sidebar:
    if os.path.exists("adidas_logo.png"):
        st.image("adidas_logo.png", width=75)
    else:
        st.markdown(ADIDAS_WHITE_LOGO_SVG, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-brand">ADIDAS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-slogan">IMPOSSIBLE IS NOTHING</div>', unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigation")
    nav_selection = st.radio(
        "View Mode",
        options=["Overview", "Products", "Regions", "Retailers"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Global Scope")
    selected_year = st.selectbox("Fiscal Year", options=["All Years", 2021, 2020], index=0)

# Main scope assignment
if selected_year != "All Years":
    df_current = raw_df[raw_df["year"] == selected_year].copy()
    prior_year = selected_year - 1
    df_prior = raw_df[raw_df["year"] == prior_year].copy()
else:
    df_current = raw_df.copy()
    df_prior = pd.DataFrame()

# ---------------------------------------------------------
# 4. Top Header & Dropdown Slicers
# ---------------------------------------------------------
col_header, col_f1, col_f2, col_f3 = st.columns([2.5, 1, 1, 1])

with col_header:
    st.markdown('<div class="header-title">Adidas Sales Dashboard</div>', unsafe_allow_html=True)
    subtitle_suffix = f"Fiscal Year: {selected_year}" if selected_year != "All Years" else "Full Multi-Year Scope (2020-2021)"
    st.markdown(
        f'<div class="header-subtitle">Performance Overview | Commercial Intelligence ({subtitle_suffix})</div>',
        unsafe_allow_html=True
    )

with col_f1:
    region_options = ["All"] + sorted(raw_df["region"].unique().tolist())
    selected_region = st.selectbox("Region", region_options, index=0)

with col_f2:
    category_options = ["All"] + sorted(raw_df["category"].unique().tolist())
    selected_category = st.selectbox("Product Category", category_options, index=0)

with col_f3:
    month_options = ["All", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    selected_month = st.selectbox("Month", month_options, index=0)

# Filter current view
filtered_df = df_current.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["month_name"] == selected_month]

# Mirror slicers on prior year
if not df_prior.empty:
    filtered_prior = df_prior.copy()
    if selected_region != "All":
        filtered_prior = filtered_prior[filtered_prior["region"] == selected_region]
    if selected_category != "All":
        filtered_prior = filtered_prior[filtered_prior["category"] == selected_category]
    if selected_month != "All":
        filtered_prior = filtered_prior[filtered_prior["month_name"] == selected_month]
else:
    filtered_prior = pd.DataFrame()

# ---------------------------------------------------------
# 5. Executive KPI Calculations (Shared Across Views)
# ---------------------------------------------------------
curr_rev = filtered_df["total_sales"].sum()
curr_prof = filtered_df["operating_profit"].sum()
curr_units = filtered_df["units_sold"].sum()
curr_margin = (curr_prof / curr_rev * 100) if curr_rev > 0 else 0.0

if not filtered_prior.empty:
    prior_rev = filtered_prior["total_sales"].sum()
    prior_prof = filtered_prior["operating_profit"].sum()
    prior_units = filtered_prior["units_sold"].sum()
    prior_margin = (prior_prof / prior_rev * 100) if prior_rev > 0 else 0.0

    rev_yoy = ((curr_rev - prior_rev) / prior_rev * 100) if prior_rev > 0 else 0.0
    prof_yoy = ((curr_prof - prior_prof) / prior_prof * 100) if prior_rev > 0 else 0.0
    units_yoy = ((curr_units - prior_units) / prior_units * 100) if prior_units > 0 else 0.0
    margin_diff = curr_margin - prior_margin
else:
    rev_yoy, prof_yoy, units_yoy, margin_diff = 0.0, 0.0, 0.0, 0.0

def format_delta(delta_val, is_pct_point=False):
    prefix = "+" if delta_val >= 0 else ""
    css_class = "delta-positive" if delta_val >= 0 else "delta-negative"
    icon = "▲" if delta_val >= 0 else "▼"
    unit = " pts" if is_pct_point else "%"
    return f'<span class="{css_class}">{icon} {prefix}{delta_val:.1f}{unit} vs LY</span>'

# Render Top 4 KPI Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 Total Revenue</div>
            <div class="kpi-value">${curr_rev / 1e6:.1f}M</div>
            <div class="kpi-delta">{format_delta(rev_yoy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💼 Total Profit</div>
            <div class="kpi-value">${curr_prof / 1e6:.1f}M</div>
            <div class="kpi-delta">{format_delta(prof_yoy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Units Sold</div>
            <div class="kpi-value">{curr_units / 1e6:.2f}M</div>
            <div class="kpi-delta">{format_delta(units_yoy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">⭐ Operating Margin</div>
            <div class="kpi-value">{curr_margin:.1f}%</div>
            <div class="kpi-delta">{format_delta(margin_diff, is_pct_point=True)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# 6. Main Page Navigation Tabs
# ---------------------------------------------------------
tab_overview, tab_pricing = st.tabs(["📊 Executive Overview", "🏷️ Pricing Elasticity & Products"])

with tab_overview:
    # Middle Row (Trend + Donut)
    m_col1, m_col2 = st.columns([1.6, 1.0])
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    with m_col1:
        monthly_summary = (
            filtered_df.groupby("month_name")[["total_sales", "operating_profit"]]
            .sum()
            .reindex(month_order)
            .fillna(0)
            .reset_index()
        )

        fig_trend = go.Figure()
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_summary["month_name"],
                y=monthly_summary["total_sales"] / 1e6,
                name="Revenue",
                mode="lines+markers",
                line=dict(color="#F8FAFC", width=3),
                marker=dict(size=7, color="#FFFFFF"),
                fill="tozeroy",
                fillcolor="rgba(248, 250, 252, 0.05)",
            )
        )
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_summary["month_name"],
                y=monthly_summary["operating_profit"] / 1e6,
                name="Profit",
                mode="lines+markers",
                line=dict(color="#64748B", width=2, dash="dot"),
                marker=dict(size=6, color="#94A3B8"),
            )
        )
        fig_trend.update_layout(
            title="<b>Revenue & Profit Trajectory</b>",
            title_font=dict(size=14, color="#FFFFFF"),
            paper_bgcolor="#14161D",
            plot_bgcolor="#14161D",
            margin=dict(l=40, r=20, t=45, b=35),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#94A3B8")),
            xaxis=dict(showgrid=False, color="#64748B", tickfont=dict(color="#94A3B8", size=11)),
            yaxis=dict(showgrid=True, gridcolor="#232733", color="#64748B", ticksuffix="M", tickprefix="$", tickfont=dict(color="#94A3B8", size=11)),
            hovermode="x unified",
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with m_col2:
        cat_summary = (
            filtered_df.groupby("category")["total_sales"]
            .sum()
            .reset_index()
            .sort_values(by="total_sales", ascending=False)
        )
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=cat_summary["category"],
                    values=cat_summary["total_sales"],
                    hole=0.68,
                    marker=dict(colors=["#F8FAFC", "#64748B", "#334155"]),
                    textinfo="percent",
                    textfont=dict(size=12, color="#0A0A0C"),
                    hoverinfo="label+value+percent",
                )
            ]
        )
        fig_donut.update_layout(
            title="<b>Sales by Product Category</b>",
            title_font=dict(size=14, color="#FFFFFF"),
            paper_bgcolor="#14161D",
            plot_bgcolor="#14161D",
            margin=dict(l=20, r=20, t=45, b=25),
            annotations=[
                dict(
                    text=f"<b>${curr_rev / 1e6:.1f}M</b><br><span style='font-size:11px;color:#94A3B8'>Total</span>",
                    x=0.5,
                    y=0.5,
                    font_size=15,
                    font_color="#FFFFFF",
                    showarrow=False,
                )
            ],
            legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5, font=dict(color="#94A3B8", size=11)),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Bottom Row (Map + Top Products)
    b_col1, b_col2 = st.columns([1.1, 1.4])

    with b_col1:
        state_sales = filtered_df.groupby("state_code")["total_sales"].sum().reset_index()
        fig_map = px.choropleth(
            state_sales,
            locations="state_code",
            locationmode="USA-states",
            color="total_sales",
            scope="usa",
            color_continuous_scale=[[0, "#1A2234"], [0.35, "#2563EB"], [0.75, "#60A5FA"], [1, "#FFFFFF"]],
        )
        fig_map.update_layout(
            title="<b>Sales by Geography</b>",
            title_font=dict(size=14, color="#FFFFFF"),
            paper_bgcolor="#14161D",
            geo=dict(bgcolor="#14161D", lakecolor="#14161D", landcolor="#0F1219", subunitcolor="#232733", showlakes=True, showland=True, showsubunits=True),
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=45, b=0),
            height=330,
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with b_col2:
        prod_summary = (
            filtered_df.groupby("product")["total_sales"]
            .sum()
            .reset_index()
            .sort_values(by="total_sales", ascending=True)
        )
        max_prod_sales = (prod_summary["total_sales"].max() / 1e6) * 1.18

        fig_bar = go.Figure(
            go.Bar(
                x=prod_summary["total_sales"] / 1e6,
                y=prod_summary["product"],
                orientation="h",
                marker=dict(color="#F8FAFC", line=dict(color="#232733", width=1)),
                text=[f"  ${v:.1f}M" for v in (prod_summary["total_sales"] / 1e6)],
                textposition="outside",
                textfont=dict(color="#FFFFFF", size=11, family="Arial"),
            )
        )
        fig_bar.update_layout(
            title="<b>Best-Selling Product Lines (by Revenue)</b>",
            title_font=dict(size=14, color="#FFFFFF"),
            paper_bgcolor="#14161D",
            plot_bgcolor="#14161D",
            margin=dict(l=20, r=80, t=45, b=25),
            height=330,
            xaxis=dict(showgrid=True, gridcolor="#232733", color="#64748B", ticksuffix="M", tickprefix="$", tickfont=dict(color="#94A3B8", size=11), range=[0, max_prod_sales]),
            yaxis=dict(showgrid=False, color="#E2E8F0", tickfont=dict(color="#FFFFFF", size=11)),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with tab_pricing:
    # 1. Executive Strategy Callout
    st.markdown(
        """
        <div style="background-color: #14161D; border-left: 4px solid #38BDF8; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
            <div style="font-weight: 700; color: #FFFFFF; font-size: 0.95rem; margin-bottom: 2px;">💡 Pricing Strategy Insight: The $50 – $70 Sweet Spot</div>
            <div style="color: #94A3B8; font-size: 0.84rem; line-height: 1.4;">
                The <b>Premium tier ($50–$70)</b> is the primary margin engine, driving <b>41.1% of all revenue ($49.4M)</b> at the highest profit margin of <b>29.5%</b>. In contrast, pricing above $70 experiences steep volume drop-off with compressed margins (26.4%).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. 4 Price-Tier Metric Cards
    tier_summary = filtered_df.copy()
    tier_summary["tier"] = pd.cut(
        tier_summary["price_per_unit"],
        bins=[0, 35, 50, 70, 150],
        labels=["Budget (<$35)", "Core ($35-$50)", "Premium ($50-$70)", "High-End ($70+)"]
    )
    perf_table = tier_summary.groupby("tier", observed=False).agg(
        Total_Revenue=("total_sales", "sum"),
        Total_Profit=("operating_profit", "sum"),
        Units_Sold=("units_sold", "sum"),
        Avg_Price=("price_per_unit", "mean")
    ).reset_index()
    perf_table["Margin_%"] = (perf_table["Total_Profit"] / perf_table["Total_Revenue"] * 100).round(1)
    perf_table["Revenue_$M"] = (perf_table["Total_Revenue"] / 1e6).round(2)
    perf_table["Avg_Price_$"] = perf_table["Avg_Price"].round(2)

    tc1, tc2, tc3, tc4 = st.columns(4)
    tier_cols = [tc1, tc2, tc3, tc4]
    tier_accent = ["#64748B", "#38BDF8", "#10B981", "#A855F7"]

    for i, row in perf_table.iterrows():
        with tier_cols[i]:
            st.markdown(
                f"""
                <div style="background-color: #14161D; border: 1px solid #232733; border-top: 3px solid {tier_accent[i]}; border-radius: 10px; padding: 14px 16px; margin-bottom: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">{row['tier']}</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #FFFFFF; margin: 4px 0;">${row['Revenue_$M']}M</div>
                    <div style="font-size: 0.80rem; color: #CBD5E1; display: flex; justify-content: space-between; margin-top: 6px;">
                        <span>Units: <b>{row['Units_Sold']:,}</b></span>
                        <span style="color: {tier_accent[i]}; font-weight: 700;">{row['Margin_%']}% Margin</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # 3. Two Side-by-Side Analytics Charts
    c_chart1, c_chart2 = st.columns([1.5, 1.0])

    with c_chart1:
        # Add slight horizontal jitter to discrete prices for clear visibility
        scatter_data = filtered_df.copy()
        scatter_data["price_jittered"] = scatter_data["price_per_unit"] + np.random.normal(0, 0.45, len(scatter_data))

        fig_scatter = px.scatter(
            scatter_data,
            x="price_jittered",
            y="units_sold",
            color="product",
            size="total_sales",
            hover_name="product",
            hover_data={"price_jittered": False, "price_per_unit": ":$.2f", "units_sold": ":,", "total_sales": ":$,.0f", "sales_method": True},
            labels={"price_jittered": "Unit Price ($)", "units_sold": "Units Sold per Transaction"},
            color_discrete_sequence=["#F8FAFC", "#38BDF8", "#F59E0B", "#10B981", "#A855F7", "#EC4899"],
        )
        fig_scatter.update_layout(
            title="<b>Price Elasticity & Transaction Size Distribution</b>",
            title_font=dict(size=14, color="#FFFFFF"),
            paper_bgcolor="#14161D",
            plot_bgcolor="#14161D",
            font=dict(color="#94A3B8"),
            margin=dict(l=40, r=20, t=45, b=35),
            height=370,
            xaxis=dict(showgrid=True, gridcolor="#232733", tickprefix="$", color="#64748B"),
            yaxis=dict(showgrid=True, gridcolor="#232733", color="#64748B"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c_chart2:
        # Product Margin vs Average Price Comparison
        prod_perf = filtered_df.groupby("product").agg(
            avg_price=("price_per_unit", "mean"),
            margin=("operating_profit", lambda x: (x.sum() / filtered_df.loc[x.index, "total_sales"].sum()) * 100),
            rev=("total_sales", "sum")
        ).reset_index()

        fig_bubble = px.scatter(
            prod_perf,
            x="avg_price",
            y="margin",
            size="rev",
            color="product",
            text="product",
            color_discrete_sequence=["#F8FAFC", "#38BDF8", "#F59E0B", "#10B981", "#A855F7", "#EC4899"]
        )
        fig_bubble.update_traces(textposition="top center", textfont=dict(size=9, color="#CBD5E1"))
        fig_bubble.update_layout(
            title="<b>Product Margin % vs Average Price</b>",
            title_font=dict(size=14, color="#FFFFFF"),
            paper_bgcolor="#14161D",
            plot_bgcolor="#14161D",
            showlegend=False,
            margin=dict(l=40, r=20, t=45, b=35),
            height=370,
            xaxis=dict(showgrid=True, gridcolor="#232733", tickprefix="$", color="#64748B"),
            yaxis=dict(showgrid=True, gridcolor="#232733", ticksuffix="%", color="#64748B"),
        )
        st.plotly_chart(fig_bubble, use_container_width=True)