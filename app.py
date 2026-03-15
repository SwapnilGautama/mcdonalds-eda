import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_loader import load_menu, load_stores, load_merged

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="McDonald's EDA Dashboard",
    page_icon="🍟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111111;
    border-right: 2px solid #DA291C;
}
section[data-testid="stSidebar"] * { color: #f5f5f5 !important; }

/* Main background */
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #222222 100%);
    border: 1px solid #333;
    border-left: 4px solid #DA291C;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.kpi-card .kpi-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 4px;
}
.kpi-card .kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 32px;
    color: #FFC72C;
    line-height: 1;
}
.kpi-card .kpi-sub {
    font-size: 11px;
    color: #666;
    margin-top: 4px;
}

/* Section headers */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    color: #DA291C;
    letter-spacing: 2px;
    border-bottom: 1px solid #333;
    padding-bottom: 8px;
    margin-bottom: 20px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #111; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: #999;
    font-weight: 500;
    padding: 8px 16px;
    font-size: 13px;
}
.stTabs [aria-selected="true"] {
    background: #DA291C !important;
    color: white !important;
}

/* Plotly chart backgrounds */
.js-plotly-plot { border-radius: 8px; }

/* Page title */
.page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 42px;
    letter-spacing: 3px;
    color: #FFC72C;
    text-shadow: 2px 2px 0px #DA291C;
    line-height: 1;
}
.page-subtitle { font-size: 13px; color: #777; letter-spacing: 1px; margin-top: 4px; }

/* India/US badge */
.badge-in { background:#FF9933; color:#000; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:700; }
.badge-us { background:#3C3B6E; color:#fff; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:700; }
.badge-all { background:#DA291C; color:#fff; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly theme ─────────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="#1a1a1a", plot_bgcolor="#1a1a1a",
        font=dict(color="#f5f5f5", family="DM Sans"),
        xaxis=dict(gridcolor="#2a2a2a", linecolor="#333"),
        yaxis=dict(gridcolor="#2a2a2a", linecolor="#333"),
        colorway=["#DA291C","#FFC72C","#FF6B35","#4ECDC4","#95E1D3","#F38181","#A8E6CF"],
    )
)
MCD_COLORS = ["#DA291C","#FFC72C","#FF6B35","#4ECDC4","#95E1D3","#F38181","#A8E6CF","#FFD93D","#6BCB77"]

# ─── Data ────────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_menu(), load_stores(), load_merged()

df_menu, df_store, df = get_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Bebas Neue;font-size:22px;color:#FFC72C;letter-spacing:2px;">🍟 McDASH</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#666;margin-bottom:16px;">McDonald\'s EDA · IITK Assignment</div>', unsafe_allow_html=True)
    st.divider()

    page = st.radio("Navigate", [
        "📊 Executive Summary",
        "🏪 Outlet Analytics",
        "🥗 Menu & Nutrition",
        "🌍 Geographic Analysis",
        "🔢 KPI Reference Table",
        "🐍 Python Query Bank",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**Filters**")
    country_filter = st.multiselect("Country", ["IN","US"], default=["IN","US"])
    ownership_filter = st.multiselect("Ownership Type",
        df_store["Ownership_Type"].unique().tolist(),
        default=df_store["Ownership_Type"].unique().tolist())
    st.divider()
    st.markdown('<div style="font-size:10px;color:#444;">Dataset: 340 outlets · 75 menu items<br>Source: IITK McDonald\'s EDA Dataset</div>', unsafe_allow_html=True)

# ─── Apply filters ────────────────────────────────────────────────────────────
df_f = df[df["Country"].isin(country_filter) & df["Ownership_Type"].isin(ownership_filter)]
df_store_f = df_store[df_store["Country"].isin(country_filter) & df_store["Ownership_Type"].isin(ownership_filter)]

def kpi_card(label, value, sub=""):
    return f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

def plot_fig(fig, height=380):
    fig.update_layout(template=None, **PLOTLY_TEMPLATE["layout"], height=height,
                      margin=dict(l=20,r=20,t=40,b=20))
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Executive Summary":
    st.markdown('<div class="page-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">HIGH-LEVEL KPIs ACROSS ALL OUTLETS & MENU ITEMS</div>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Top KPI row
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    total_rev = df_store_f["Revenue"].sum()
    total_prof = df_store_f["Profits"].sum()
    avg_gpm = df_store_f["Gross_Profit_Margin"].mean()
    total_cust = df_store_f["Customers"].sum()
    total_emp = df_store_f["Number_of_Employees"].sum()
    n_outlets = len(df_store_f)

    c1.markdown(kpi_card("Total Revenue","${:,.0f}mn".format(total_rev),"Million INR · filtered"), unsafe_allow_html=True)
    c2.markdown(kpi_card("Total Profits","${:,.0f}mn".format(total_prof),"Million INR"), unsafe_allow_html=True)
    c3.markdown(kpi_card("Avg GPM","{:.1f}%".format(avg_gpm),"Gross profit margin"), unsafe_allow_html=True)
    c4.markdown(kpi_card("Total Footfall","{:,.0f}".format(total_cust),"Total customers"), unsafe_allow_html=True)
    c5.markdown(kpi_card("Total Employees","{:,.0f}".format(total_emp),"Headcount"), unsafe_allow_html=True)
    c6.markdown(kpi_card("Outlets",str(n_outlets),"Active in filter"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Revenue Distribution</div>', unsafe_allow_html=True)
        fig = px.histogram(df_store_f, x="Revenue", nbins=25, color="Country",
                           color_discrete_map={"IN":"#FF9933","US":"#3C3B6E"},
                           barmode="overlay", opacity=0.8,
                           labels={"Revenue":"Revenue (mn INR)"})
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(plot_fig(fig), use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Ownership Type Split</div>', unsafe_allow_html=True)
        oc = df_store_f["Ownership_Type"].value_counts().reset_index()
        oc.columns = ["Type","Count"]
        fig2 = px.pie(oc, names="Type", values="Count",
                      color_discrete_sequence=MCD_COLORS, hole=0.55)
        fig2.update_traces(textposition="outside", textinfo="label+percent",
                           textfont_size=11)
        st.plotly_chart(plot_fig(fig2, 360), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Revenue vs Profit by Country</div>', unsafe_allow_html=True)
        fig3 = px.scatter(df_store_f, x="Revenue", y="Profits", color="Country",
                          size="Customers", hover_name="Store_Name",
                          color_discrete_map={"IN":"#FF9933","US":"#4ECDC4"},
                          size_max=20, opacity=0.75,
                          labels={"Revenue":"Revenue (mn INR)","Profits":"Profits (mn INR)"})
        st.plotly_chart(plot_fig(fig3), use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Revenue by Ownership Type</div>', unsafe_allow_html=True)
        rev_own = df_store_f.groupby("Ownership_Type")["Revenue"].agg(["mean","min","max"]).reset_index()
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Avg Revenue", x=rev_own["Ownership_Type"], y=rev_own["mean"],
                              marker_color="#DA291C"))
        fig4.add_trace(go.Scatter(name="Max Revenue", x=rev_own["Ownership_Type"], y=rev_own["max"],
                                  mode="markers", marker=dict(color="#FFC72C", size=12, symbol="diamond")))
        fig4.update_layout(barmode="group", legend=dict(x=0.7,y=1))
        st.plotly_chart(plot_fig(fig4), use_container_width=True)

    st.markdown('<div class="section-header">Key Insights</div>', unsafe_allow_html=True)
    i1,i2,i3,i4 = st.columns(4)
    i1.info("🇺🇸 **US outlets** account for **95.8%** of total revenue despite being 75.9% of outlets")
    i2.warning("🤝 **All India outlets** operate as **Joint Ventures** (CPRL & Hardcastle) — zero company-owned")
    i3.success("📈 **Salad-selling outlets** earn the **highest avg revenue** despite salads being only 1.8% of the menu")
    i4.error("📉 **Negative GPM** found in several outlets — Cost Price exceeds Selling Price in high-footfall stores")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — OUTLET ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏪 Outlet Analytics":
    st.markdown('<div class="page-title">Outlet Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">STORE-LEVEL KPIs — REVENUE · PROFIT · EMPLOYEES · FOOTFALL</div>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Revenue & Profit", "Employees & Footfall", "Top 10 Rankings", "Detailed Table"])

    with tab1:
        c1,c2,c3,c4 = st.columns(4)
        c1.markdown(kpi_card("Avg Revenue","{:.1f} mn".format(df_store_f["Revenue"].mean()),"Per outlet"), unsafe_allow_html=True)
        c2.markdown(kpi_card("Avg Profit","{:.2f} mn".format(df_store_f["Profits"].mean()),"Per outlet"), unsafe_allow_html=True)
        c3.markdown(kpi_card("Max Revenue","{:.1f} mn".format(df_store_f["Revenue"].max()),"Single outlet"), unsafe_allow_html=True)
        c4.markdown(kpi_card("Avg GPM","{:.2f}%".format(df_store_f["Gross_Profit_Margin"].mean()),"Gross profit margin"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Revenue by Country</div>', unsafe_allow_html=True)
            rev_country = df_store_f.groupby("Country")["Revenue"].agg(
                Total="sum", Average="mean", Median="median").reset_index()
            fig = go.Figure()
            for metric, color in zip(["Total","Average","Median"],["#DA291C","#FFC72C","#4ECDC4"]):
                fig.add_trace(go.Bar(name=metric, x=rev_country["Country"],
                                     y=rev_country[metric], marker_color=color))
            fig.update_layout(barmode="group")
            st.plotly_chart(plot_fig(fig), use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">Gross Profit Margin Distribution</div>', unsafe_allow_html=True)
            fig2 = px.box(df_store_f, x="Country", y="Gross_Profit_Margin", color="Country",
                          color_discrete_map={"IN":"#FF9933","US":"#4ECDC4"},
                          points="all",
                          labels={"Gross_Profit_Margin":"GPM (%)"})
            fig2.add_hline(y=0, line_dash="dash", line_color="#666", annotation_text="Break-even GPM")
            st.plotly_chart(plot_fig(fig2), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-header">Revenue vs Cost Price</div>', unsafe_allow_html=True)
            fig3 = px.scatter(df_store_f, x="Cost_Price", y="Revenue", color="Ownership_Type",
                              hover_name="Store_Name", trendline="ols",
                              color_discrete_sequence=MCD_COLORS,
                              labels={"Cost_Price":"Cost Price (mn INR)","Revenue":"Revenue (mn INR)"})
            st.plotly_chart(plot_fig(fig3), use_container_width=True)

        with col4:
            st.markdown('<div class="section-header">Selling Price vs Cost Price by Category</div>', unsafe_allow_html=True)
            if "Category" in df_f.columns:
                cp_cat = df_f.groupby("Category")[["Selling_Price","Cost_Price"]].mean().reset_index().sort_values("Selling_Price")
                fig4 = go.Figure()
                fig4.add_trace(go.Bar(name="Selling Price", y=cp_cat["Category"],
                                      x=cp_cat["Selling_Price"], orientation="h", marker_color="#FFC72C"))
                fig4.add_trace(go.Bar(name="Cost Price", y=cp_cat["Category"],
                                      x=cp_cat["Cost_Price"], orientation="h", marker_color="#DA291C"))
                fig4.update_layout(barmode="group")
                st.plotly_chart(plot_fig(fig4, 420), use_container_width=True)

    with tab2:
        c1,c2,c3,c4 = st.columns(4)
        c1.markdown(kpi_card("Total Footfall","{:,.0f}".format(df_store_f["Customers"].sum()),"All outlets"), unsafe_allow_html=True)
        c2.markdown(kpi_card("Avg Footfall","{:,.0f}".format(df_store_f["Customers"].mean()),"Per outlet"), unsafe_allow_html=True)
        c3.markdown(kpi_card("Total Employees","{:,.0f}".format(df_store_f["Number_of_Employees"].sum()),"All outlets"), unsafe_allow_html=True)
        c4.markdown(kpi_card("Avg Employees","{:.0f}".format(df_store_f["Number_of_Employees"].mean()),"Per outlet"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Employees by Ownership & Country</div>', unsafe_allow_html=True)
            emp_grp = df_store_f.groupby(["Ownership_Type","Country"])["Number_of_Employees"].mean().reset_index()
            fig = px.bar(emp_grp, x="Ownership_Type", y="Number_of_Employees", color="Country",
                         barmode="group", color_discrete_map={"IN":"#FF9933","US":"#4ECDC4"},
                         labels={"Number_of_Employees":"Avg Employees"})
            st.plotly_chart(plot_fig(fig), use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">Footfall vs Revenue</div>', unsafe_allow_html=True)
            fig2 = px.scatter(df_store_f, x="Customers", y="Revenue", color="Country",
                              hover_name="Store_Name", size="Number_of_Employees",
                              color_discrete_map={"IN":"#FF9933","US":"#4ECDC4"},
                              labels={"Customers":"Customer Footfall","Revenue":"Revenue (mn INR)"})
            st.plotly_chart(plot_fig(fig2), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-header">Revenue per Employee</div>', unsafe_allow_html=True)
            df_store_f2 = df_store_f.copy()
            df_store_f2["Rev_per_Emp"] = df_store_f2["Revenue"] / df_store_f2["Number_of_Employees"]
            fig3 = px.histogram(df_store_f2, x="Rev_per_Emp", color="Country", nbins=20,
                                color_discrete_map={"IN":"#FF9933","US":"#4ECDC4"},
                                labels={"Rev_per_Emp":"Revenue per Employee (mn INR)"})
            st.plotly_chart(plot_fig(fig3), use_container_width=True)

        with col4:
            st.markdown('<div class="section-header">Employee Distribution by Country</div>', unsafe_allow_html=True)
            fig4 = px.violin(df_store_f, x="Country", y="Number_of_Employees", color="Country",
                             box=True, points="all",
                             color_discrete_map={"IN":"#FF9933","US":"#4ECDC4"})
            st.plotly_chart(plot_fig(fig4), use_container_width=True)

    with tab3:
        st.markdown('<div class="section-header">Top 10 Rankings</div>', unsafe_allow_html=True)
        metric = st.selectbox("Rank by", ["Revenue","Profits","Customers","Number_of_Employees","Gross_Profit_Margin"])
        top10 = df_store_f.nlargest(10, metric)[["Store_Name","City","State","Country","Ownership_Type", metric]].reset_index(drop=True)
        top10.index += 1

        fig = px.bar(top10, x=metric, y="Store_Name", orientation="h",
                     color="Country", color_discrete_map={"IN":"#FF9933","US":"#DA291C"},
                     text=metric, hover_data=["City","State","Ownership_Type"])
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(plot_fig(fig, 430), use_container_width=True)
        st.dataframe(top10, use_container_width=True)

    with tab4:
        st.markdown('<div class="section-header">Full Outlet Table</div>', unsafe_allow_html=True)
        show_cols = ["Store_Name","Ownership_Type","City","State","Country",
                     "Revenue","Profits","Gross_Profit_Margin","Number_of_Employees","Customers"]
        sort_col = st.selectbox("Sort by", ["Revenue","Profits","Customers"], key="sort_full")
        display = df_store_f[show_cols].sort_values(sort_col, ascending=False).reset_index(drop=True)
        display.index += 1
        st.dataframe(display.style.background_gradient(subset=["Revenue","Profits"], cmap="Reds")
                     .format({"Revenue":"{:.3f}","Profits":"{:.3f}","Gross_Profit_Margin":"{:.2f}%"}),
                     use_container_width=True, height=500)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — MENU & NUTRITION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🥗 Menu & Nutrition":
    st.markdown('<div class="page-title">Menu & Nutrition</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">75 MENU ITEMS · 14 CATEGORIES · NUTRITIONAL DEEP DIVE</div>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Category Overview", "Nutrient Breakdown", "Item Explorer", "Grilled vs Crispy"])

    with tab1:
        c1,c2,c3,c4 = st.columns(4)
        c1.markdown(kpi_card("Menu Items","75","Total items in dataset"), unsafe_allow_html=True)
        c2.markdown(kpi_card("Categories","14","Distinct food categories"), unsafe_allow_html=True)
        c3.markdown(kpi_card("Avg Calories","{:.0f} kcal".format(df_menu["Energy"].mean()),"Per item"), unsafe_allow_html=True)
        c4.markdown(kpi_card("Max Protein","87 g","Chicken McNuggets 40pc"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Items per Category</div>', unsafe_allow_html=True)
            cat_count = df_menu["Category"].value_counts().reset_index()
            cat_count.columns = ["Category","Count"]
            fig = px.bar(cat_count, x="Count", y="Category", orientation="h",
                         color="Count", color_continuous_scale=["#333","#DA291C","#FFC72C"])
            fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
            st.plotly_chart(plot_fig(fig, 420), use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">Avg Calories by Category</div>', unsafe_allow_html=True)
            cal_cat = df_menu.groupby("Category")["Energy"].median().sort_values().reset_index()
            fig2 = px.bar(cal_cat, x="Energy", y="Category", orientation="h",
                          color="Energy", color_continuous_scale=["#1a6e1a","#FFC72C","#DA291C"],
                          labels={"Energy":"Median Calories (kcal)"})
            fig2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(plot_fig(fig2, 420), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-header">Avg Sugar by Category</div>', unsafe_allow_html=True)
            sug_cat = df_menu.groupby("Category")["Sugars"].mean().sort_values(ascending=False).reset_index()
            fig3 = px.bar(sug_cat, x="Category", y="Sugars",
                          color="Sugars", color_continuous_scale=["#1a4e1a","#FFC72C","#DA291C"])
            fig3.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
            st.plotly_chart(plot_fig(fig3), use_container_width=True)

        with col4:
            st.markdown('<div class="section-header">Avg Dietary Fibre by Category</div>', unsafe_allow_html=True)
            fib_cat = df_menu.groupby("Category")["Dietary_Fibre"].mean().sort_values(ascending=False).reset_index()
            fig4 = px.bar(fib_cat, x="Category", y="Dietary_Fibre",
                          color="Dietary_Fibre", color_continuous_scale=["#222","#4ECDC4","#95E1D3"])
            fig4.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
            st.plotly_chart(plot_fig(fig4), use_container_width=True)

    with tab2:
        st.markdown('<div class="section-header">Nutrient Comparison Across Categories</div>', unsafe_allow_html=True)
        nutrient = st.selectbox("Select Nutrient", ["Energy","Protein","Total_Fat","Saturated_Fat",
                                                     "Trans_Fat","Cholestrol","Carbohydrates","Sugars",
                                                     "Dietary_Fibre","Sodium"])
        fig = px.box(df_menu, x="Category", y=nutrient, color="Category",
                     color_discrete_sequence=MCD_COLORS, points="all",
                     labels={nutrient: nutrient.replace("_"," ")})
        fig.update_layout(xaxis_tickangle=-35, showlegend=False)
        st.plotly_chart(plot_fig(fig, 450), use_container_width=True)

        st.markdown('<div class="section-header">Nutritious vs Non-Nutritious Score (Top 20 Items)</div>', unsafe_allow_html=True)
        top20 = df_menu.nlargest(20, "Nutritious")[["Item","Category","Nutritious","Non_Nutritious","Energy"]]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Nutritious (Protein+Fibre)", y=top20["Item"],
                              x=top20["Nutritious"], orientation="h", marker_color="#4ECDC4"))
        fig2.add_trace(go.Bar(name="Non-Nutritious (Fat+SatFat+TransFat+Chol)", y=top20["Item"],
                              x=top20["Non_Nutritious"], orientation="h", marker_color="#DA291C"))
        fig2.update_layout(barmode="group", yaxis=dict(autorange="reversed"), height=520)
        st.plotly_chart(plot_fig(fig2, 520), use_container_width=True)

    with tab3:
        st.markdown('<div class="section-header">Item Explorer</div>', unsafe_allow_html=True)
        cat_sel = st.multiselect("Filter Category", df_menu["Category"].unique().tolist(),
                                  default=["Breakfast","Beef & Pork","Salads"])
        items_view = df_menu[df_menu["Category"].isin(cat_sel)].copy()
        x_axis = st.selectbox("X Axis", ["Energy","Protein","Total_Fat","Carbohydrates","Sugars","Sodium"], key="x")
        y_axis = st.selectbox("Y Axis", ["Protein","Energy","Total_Fat","Dietary_Fibre","Sugars"], index=1, key="y")

        fig = px.scatter(items_view, x=x_axis, y=y_axis, color="Category",
                         size="Serve_Size", hover_name="Item",
                         size_max=25, color_discrete_sequence=MCD_COLORS,
                         labels={x_axis: x_axis.replace("_"," "), y_axis: y_axis.replace("_"," ")})
        st.plotly_chart(plot_fig(fig, 460), use_container_width=True)

        st.dataframe(items_view[["Category","Item","Energy","Protein","Total_Fat",
                                  "Sugars","Dietary_Fibre","Sodium","Nutritious","Non_Nutritious"]]
                     .sort_values("Nutritious", ascending=False).reset_index(drop=True),
                     use_container_width=True)

    with tab4:
        st.markdown('<div class="section-header">Grilled vs Crispy — Fat Comparison</div>', unsafe_allow_html=True)
        grilled = df_menu[df_menu["Grilled"]].copy()
        grilled_names = grilled["Item"].str.replace("Grilled","Crispy", regex=False)
        crispy = df_menu[df_menu["Item"].isin(grilled_names)].copy()

        if len(grilled) > 0 and len(crispy) > 0:
            comp_df = pd.DataFrame({
                "Item": grilled["Item"].str.replace("Grilled","", regex=False).str.strip().values[:len(crispy)],
                "Grilled_Fat": grilled["Total_Fat"].values[:len(crispy)],
                "Crispy_Fat": crispy["Total_Fat"].values[:len(crispy)],
            })
            comp_df["Fat_Diff"] = comp_df["Crispy_Fat"] - comp_df["Grilled_Fat"]
            comp_df["Pct_More"] = (comp_df["Fat_Diff"] / comp_df["Grilled_Fat"] * 100).round(1)

            fig = go.Figure()
            fig.add_trace(go.Bar(name="Grilled (g fat)", y=comp_df["Item"],
                                  x=comp_df["Grilled_Fat"], orientation="h",
                                  marker_color="#4ECDC4"))
            fig.add_trace(go.Bar(name="Crispy (g fat)", y=comp_df["Item"],
                                  x=comp_df["Crispy_Fat"], orientation="h",
                                  marker_color="#DA291C"))
            fig.update_layout(barmode="group", yaxis=dict(autorange="reversed"))
            st.plotly_chart(plot_fig(fig, 400), use_container_width=True)

            st.info(f"On average, Crispy variants have **{comp_df['Pct_More'].mean():.0f}% more fat** than their Grilled equivalents.")
            st.dataframe(comp_df.style.background_gradient(subset=["Fat_Diff"], cmap="RdYlGn_r")
                         .format({"Grilled_Fat":"{:.1f}g","Crispy_Fat":"{:.1f}g",
                                   "Fat_Diff":"+{:.1f}g","Pct_More":"{:.1f}%"}),
                         use_container_width=True)
        else:
            st.info("Select menu items with 'Grilled' in the name to compare.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — GEOGRAPHIC ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🌍 Geographic Analysis":
    st.markdown('<div class="page-title">Geographic Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">OUTLET DISTRIBUTION · REVENUE BY LOCATION · INDIA vs US</div>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["World Map", "India Focus", "US Focus"])

    with tab1:
        st.markdown('<div class="section-header">All Outlet Locations</div>', unsafe_allow_html=True)
        map_metric = st.selectbox("Bubble size", ["Revenue","Profits","Customers","Number_of_Employees"])
        fig = px.scatter_geo(df_store_f, lat="Latitude", lon="Longitude",
                             color="Country", size=map_metric,
                             hover_name="Store_Name",
                             hover_data={"Revenue":True,"Profits":True,"Ownership_Type":True},
                             color_discrete_map={"IN":"#FF9933","US":"#4ECDC4"},
                             size_max=25, projection="natural earth")
        fig.update_layout(geo=dict(bgcolor="#1a1a1a", landcolor="#2a2a2a",
                                    oceancolor="#111", showocean=True,
                                    coastlinecolor="#444", showcoastlines=True),
                          paper_bgcolor="#1a1a1a", height=480, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Top 10 Cities by Outlet Count</div>', unsafe_allow_html=True)
            city_cnt = df_store_f["City"].value_counts().head(10).reset_index()
            city_cnt.columns = ["City","Count"]
            fig2 = px.bar(city_cnt, x="Count", y="City", orientation="h",
                          color="Count", color_continuous_scale=["#333","#DA291C"])
            fig2.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
            st.plotly_chart(plot_fig(fig2, 360), use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">Top 10 States by Outlet Count</div>', unsafe_allow_html=True)
            state_cnt = df_store_f["State"].value_counts().head(10).reset_index()
            state_cnt.columns = ["State","Count"]
            fig3 = px.bar(state_cnt, x="Count", y="State", orientation="h",
                          color="Count", color_continuous_scale=["#333","#FFC72C"])
            fig3.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
            st.plotly_chart(plot_fig(fig3, 360), use_container_width=True)

    with tab2:
        st.markdown('<div class="section-header">India Outlet Map</div>', unsafe_allow_html=True)
        india = df_store_f[df_store_f["Country"] == "IN"]
        if len(india) > 0:
            fig = px.scatter_geo(india, lat="Latitude", lon="Longitude",
                                 size="Revenue", color="Revenue",
                                 hover_name="Store_Name",
                                 hover_data={"City":True,"Profits":True,"Customers":True},
                                 color_continuous_scale=["#1a1a1a","#FF9933","#FFC72C"],
                                 size_max=30, scope="asia")
            fig.update_layout(geo=dict(bgcolor="#1a1a1a", landcolor="#2a2a2a",
                                        oceancolor="#111", showocean=True,
                                        coastlinecolor="#444"),
                              paper_bgcolor="#1a1a1a", height=450,
                              margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                india_city = india.groupby("City")["Revenue"].agg(["sum","mean","count"]).reset_index()
                india_city.columns = ["City","Total Revenue","Avg Revenue","Outlets"]
                india_city = india_city.sort_values("Total Revenue", ascending=False)
                fig2 = px.bar(india_city, x="City", y="Total Revenue",
                              color="Outlets", color_continuous_scale=["#333","#FF9933"],
                              labels={"Total Revenue":"Total Revenue (mn INR)"})
                st.plotly_chart(plot_fig(fig2), use_container_width=True)
            with col2:
                st.dataframe(india[["Store_Name","City","State","Revenue","Profits",
                                     "Gross_Profit_Margin","Customers"]].sort_values("Revenue",ascending=False)
                             .reset_index(drop=True), use_container_width=True, height=350)
        else:
            st.warning("No India outlets in current filter.")

    with tab3:
        st.markdown('<div class="section-header">US Outlet Map</div>', unsafe_allow_html=True)
        us = df_store_f[df_store_f["Country"] == "US"]
        if len(us) > 0:
            fig = px.scatter_geo(us, lat="Latitude", lon="Longitude",
                                 size="Revenue", color="Ownership_Type",
                                 hover_name="Store_Name",
                                 hover_data={"City":True,"State":True,"Revenue":True},
                                 color_discrete_sequence=MCD_COLORS,
                                 size_max=25, scope="usa")
            fig.update_layout(geo=dict(bgcolor="#1a1a1a", landcolor="#2a2a2a",
                                        lakecolor="#111", showlakes=True),
                              paper_bgcolor="#1a1a1a", height=430,
                              margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="section-header">Avg Revenue by US State</div>', unsafe_allow_html=True)
            state_rev = us.groupby("State")["Revenue"].mean().reset_index().sort_values("Revenue",ascending=False).head(15)
            fig2 = px.bar(state_rev, x="State", y="Revenue",
                          color="Revenue", color_continuous_scale=["#333","#4ECDC4","#FFC72C"],
                          labels={"Revenue":"Avg Revenue (mn INR)"})
            fig2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(plot_fig(fig2), use_container_width=True)
        else:
            st.warning("No US outlets in current filter.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — KPI REFERENCE TABLE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔢 KPI Reference Table":
    st.markdown('<div class="page-title">KPI Reference Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">ALL 78 KPIs WITH FORMULAS & CALCULATED VALUES</div>', unsafe_allow_html=True)
    st.markdown("---")

    kpi_data = [
        # Outlet Financial
        ["Outlet Financial","Total Revenue","SUM(Revenue)","8,790 mn INR","371.5 mn INR","8,419 mn INR"],
        ["Outlet Financial","Avg Revenue per Outlet","MEAN(Revenue)","25.85 mn INR","4.53 mn INR","32.63 mn INR"],
        ["Outlet Financial","Median Revenue","MEDIAN(Revenue)","27.06 mn INR","3.74 mn INR","33.87 mn INR"],
        ["Outlet Financial","Min Revenue","MIN(Revenue)","1.001 mn INR","1.001 mn INR","7.98 mn INR"],
        ["Outlet Financial","Max Revenue","MAX(Revenue)","49.68 mn INR","9.92 mn INR","49.68 mn INR"],
        ["Outlet Financial","Total Profits","SUM(Profits)","1,577 mn INR","75.8 mn INR","1,501 mn INR"],
        ["Outlet Financial","Avg Profit per Outlet","MEAN(Profits)","4.64 mn INR","0.924 mn INR","5.82 mn INR"],
        ["Outlet Financial","Min Profit","MIN(Profits)","0.050 mn INR","0.050 mn INR","0.887 mn INR"],
        ["Outlet Financial","Max Profit","MAX(Profits)","13.51 mn INR","2.95 mn INR","13.51 mn INR"],
        ["Outlet Financial","Avg Gross Profit Margin","MEAN(GPM)","3.52%","0.55%","4.52%"],
        ["Outlet Financial","Min GPM","MIN(GPM)","-4.88%","-1.23%","-4.88%"],
        ["Outlet Financial","Max GPM","MAX(GPM)","19.46%","0.94%","19.46%"],
        ["Outlet Financial","Avg Revenue per Employee","MEAN(Revenue/Employees)","0.287 mn","0.092 mn","0.305 mn"],
        ["Outlet Financial","Avg Revenue per Customer","MEAN(Revenue/Customers)","0.00198 mn","0.000629 mn","0.00212 mn"],
        ["Outlet Financial","Avg Selling Price","MEAN(Selling_Price)","14.60 mn","2.22 mn","18.34 mn"],
        ["Outlet Financial","Avg Cost Price","MEAN(Cost_Price)","11.08 mn","1.67 mn","13.93 mn"],
        # Outlet Operations
        ["Outlet Operations","Total Outlets","COUNT(Store_ID)","340","82 (24.1%)","258 (75.9%)"],
        ["Outlet Operations","Company Owned Outlets","COUNT WHERE Ownership='Company Owned'","137 (40.3%)","0","137"],
        ["Outlet Operations","Licensed Outlets","COUNT WHERE Ownership='Licensed'","121 (35.6%)","0","121"],
        ["Outlet Operations","Joint Venture Outlets","COUNT WHERE Ownership='Joint Venture'","82 (24.1%)","82","0"],
        ["Outlet Operations","Total Footfall","SUM(Customers)","4,444,308","430,291","4,014,017"],
        ["Outlet Operations","Avg Customers per Outlet","MEAN(Customers)","13,072","5,247","15,558"],
        ["Outlet Operations","Min Customers","MIN(Customers)","1,002","1,002","1,906"],
        ["Outlet Operations","Max Customers","MAX(Customers)","24,964","24,780","24,964"],
        ["Outlet Operations","Total Employees","SUM(Employees)","30,623","2,842","27,781"],
        ["Outlet Operations","Avg Employees per Outlet","MEAN(Employees)","90.1","34.7","107.6"],
        ["Outlet Operations","Min Employees","MIN(Employees)","25","25","50"],
        ["Outlet Operations","Max Employees","MAX(Employees)","149","99","149"],
        # Outlet Ranking
        ["Outlet Ranking","Top Revenue Outlet","ARGMAX(Revenue)","19th & Telephone (Moore OK) — 49.68","Bandra East FIFC — 9.92","19th & Telephone — 49.68"],
        ["Outlet Ranking","Top Profit Outlet","ARGMAX(Profits)","Target Kansas City — 13.51","Bandra East FIFC — 2.95","Target Kansas City — 13.51"],
        ["Outlet Ranking","Top Footfall Outlet","ARGMAX(Customers)","Hwy 44 Eagle ID — 24,964","Bandra East FIFC — 24,780","Hwy 44 Eagle ID — 24,964"],
        ["Outlet Ranking","Top Employee Outlet","ARGMAX(Employees)","19th & Telephone — 149","Bandra East FIFC — 99","19th & Telephone — 149"],
        ["Outlet Ranking","Top Nutritious Best-Seller","ARGMAX(Nutritious Score)","Houston Levee & Winchester TN","—","Houston Levee & Winchester TN"],
        # Menu / Nutrition
        ["Menu / Nutrition","Total Menu Items","COUNT(Item)","75 items","—","—"],
        ["Menu / Nutrition","Menu Categories","COUNT DISTINCT(Category)","14","—","—"],
        ["Menu / Nutrition","Largest Category","ARGMAX(COUNT by Category)","Hot Beverages — 99 items (29%)","—","—"],
        ["Menu / Nutrition","Smallest Category","ARGMIN(COUNT by Category)","Chicken Wings — 2 items (0.6%)","—","—"],
        ["Menu / Nutrition","Avg Energy","MEAN(Energy)","337.8 kcal","~210 kcal","~385 kcal"],
        ["Menu / Nutrition","Median Energy","MEDIAN(Energy)","299.5 kcal","—","—"],
        ["Menu / Nutrition","Max Energy","MAX(Energy)","1,880 kcal (McNuggets 40pc)","—","—"],
        ["Menu / Nutrition","Highest Calorie Category","ARGMAX(MEDIAN Energy by Cat)","Chicken & Fish — ~580 kcal","—","—"],
        ["Menu / Nutrition","Lowest Calorie Category","ARGMIN(MEDIAN Energy by Cat)","Cold Beverages — ~140 kcal","—","—"],
        ["Menu / Nutrition","Avg Protein","MEAN(Protein)","11.69 g","~8.2 g","~13.1 g"],
        ["Menu / Nutrition","Most Protein-Rich Item","ARGMAX(Protein)","McNuggets 40pc — 87g","—","—"],
        ["Menu / Nutrition","Avg Total Fat","MEAN(Total_Fat)","13.05 g","—","—"],
        ["Menu / Nutrition","Avg Sugar","MEAN(Sugars)","26.35 g","—","—"],
        ["Menu / Nutrition","Avg Sugar — Smoothies & Shakes","MEAN(Sugars) WHERE Cat='Smoothies'","~70 g","—","—"],
        ["Menu / Nutrition","Avg Dietary Fibre","MEAN(Dietary_Fibre)","1.54 g","—","—"],
        ["Menu / Nutrition","Highest Fibre Category","ARGMAX(MEAN Fibre by Cat)","Salads — ~4.5 g","—","—"],
        ["Menu / Nutrition","Avg Sodium","MEAN(Sodium)","481.8 mg","~310 mg","~535 mg"],
        ["Menu / Nutrition","Avg Cholesterol","MEAN(Cholestrol)","47.54 mg","—","—"],
        ["Menu / Nutrition","Avg Carbohydrates","MEAN(Carbohydrates)","43.77 g","—","—"],
        # Nutritional Index
        ["Nutritional Index","Nutritious Score Max","MAX(Protein+Dietary_Fibre)","41 g (Big Breakfast w/ Hotcakes+EggWhites Lg)","—","—"],
        ["Nutritional Index","Non-Nutritious Score Max","MAX(Fat+SatFat+TransFat+Chol)","~573 (Big Breakfast w/ Hotcakes Lg)","—","—"],
        ["Nutritional Index","Avg Nutritious by Category","MEAN(Nutritious) GROUP BY Cat","Chicken & Fish:27.5 | Salads:24 | Hot Bev:1.2","—","—"],
        # Menu Comparison
        ["Menu Comparison","Grilled vs Crispy — Avg Fat","MEAN(Fat) Grilled vs Crispy","Grilled:~15.4g | Crispy:~26.8g","—","—"],
        ["Menu Comparison","Grilled Items Count","COUNT WHERE Item CONTAINS 'Grilled'","13 items","—","—"],
        # Category-Revenue Link
        ["Category-Revenue Link","Highest Revenue Category","ARGMAX(MEAN Rev by Category)","Salads — ~35.8 mn INR avg","—","—"],
        ["Category-Revenue Link","Lowest Revenue Category","ARGMIN(MEAN Rev by Category)","Hot Beverages — ~14.0 mn INR avg","—","—"],
        ["Category-Revenue Link","Highest Selling Price Cat","ARGMAX(MEAN Selling_Price by Cat)","Beef & Pork — ~21.5 mn INR","—","—"],
        ["Category-Revenue Link","Highest Cost Price Cat","ARGMAX(MEAN Cost_Price by Cat)","Salads — ~18.2 mn INR","—","—"],
        # Geography
        ["Geography","City with Most Outlets","ARGMAX(COUNT by City)","Mumbai (India)","Mumbai","—"],
        ["Geography","State with Most Outlets","ARGMAX(COUNT by State)","MH — Maharashtra","MH","—"],
        ["Geography","Highest Revenue State (US)","ARGMAX(MEAN Rev by State WHERE US)","Oklahoma (OK) — ~38.6 mn INR","—","Oklahoma (OK)"],
        ["Geography","Unique Cities India","COUNT DISTINCT(City) WHERE IN","~12 cities","~12 cities","—"],
        ["Geography","Unique States US","COUNT DISTINCT(State) WHERE US","~35+ states","—","~35+ states"],
        # Country Comparison
        ["Country Comparison","US vs India — Avg Energy","MEAN(Energy) GROUP BY Country","337.8 kcal overall","~210 kcal","~385 kcal"],
        ["Country Comparison","US vs India — Avg Protein","MEAN(Protein) GROUP BY Country","11.69 g overall","~8.2 g","~13.1 g"],
        ["Country Comparison","US vs India — Avg Fat","MEAN(Total_Fat) GROUP BY Country","13.05 g overall","~7.5 g","~15.2 g"],
        ["Country Comparison","US vs India — Avg Sugar","MEAN(Sugars) GROUP BY Country","26.35 g overall","~18.4 g","~29.0 g"],
        ["Country Comparison","US vs India — Avg Sodium","MEAN(Sodium) GROUP BY Country","481.8 mg overall","~310 mg","~535 mg"],
        ["Country Comparison","Revenue Split US vs India","SUM(Revenue) by Country / Total","US:95.8% | India:4.2%","4.2% of total","95.8% of total"],
        # Ownership Analysis
        ["Ownership Analysis","Avg Employees — Company Owned","MEAN(Emp) WHERE Company Owned","~107 employees","—","~107"],
        ["Ownership Analysis","Avg Employees — Licensed","MEAN(Emp) WHERE Licensed","~96 employees","—","~96"],
        ["Ownership Analysis","Avg Employees — Joint Venture","MEAN(Emp) WHERE Joint Venture","~49 employees","~49","—"],
        ["Ownership Analysis","Avg Revenue — Company Owned","MEAN(Rev) WHERE Company Owned","~32.5 mn INR","—","~32.5 mn"],
        ["Ownership Analysis","Avg Revenue — Licensed","MEAN(Rev) WHERE Licensed","~31.8 mn INR","—","~31.8 mn"],
        ["Ownership Analysis","Avg Revenue — Joint Venture","MEAN(Rev) WHERE Joint Venture","~4.53 mn INR","~4.53 mn","—"],
    ]

    kpi_df = pd.DataFrame(kpi_data, columns=["Category","KPI","Formula","All Outlets","India","US"])

    cat_filter = st.multiselect("Filter by Category", kpi_df["Category"].unique().tolist(),
                                 default=kpi_df["Category"].unique().tolist())
    search = st.text_input("Search KPI", placeholder="e.g. revenue, protein, customers...")

    filtered = kpi_df[kpi_df["Category"].isin(cat_filter)]
    if search:
        filtered = filtered[filtered["KPI"].str.contains(search, case=False) |
                            filtered["Formula"].str.contains(search, case=False)]

    st.markdown(f"**Showing {len(filtered)} of {len(kpi_df)} KPIs**")
    st.dataframe(filtered.reset_index(drop=True).style
                 .apply(lambda x: ["background-color: #1f1f1f" if i%2==0 else "background-color: #181818"
                                    for i in range(len(x))], axis=0),
                 use_container_width=True, height=600)

    # Download button
    csv = filtered.to_csv(index=False)
    st.download_button("⬇ Download KPI Table as CSV", csv, "mcd_kpi_reference.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — PYTHON QUERY BANK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🐍 Python Query Bank":
    st.markdown('<div class="page-title">Python Query Bank</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">EVERY ANALYSIS IN THE NOTEBOOK — WITH CODE</div>', unsafe_allow_html=True)
    st.markdown("---")

    queries = {
        "🔧 Setup & Data Loading": [
            ("Import Libraries", """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.offline import iplot
import plotly.graph_objs as go"""),
            ("Load Datasets", """df_menu  = pd.read_excel('mcdonalds_menu.xlsx')
df_store = pd.read_excel('mcdonalds_outlets.xlsx')"""),
            ("Merge Datasets", """df_merge = pd.merge(df_store, df_menu,
    how='inner',
    left_on='Best_Selling_Item',
    right_on='Item'
).drop(['Item'], axis=1)"""),
            ("Basic Info", """df_merge.info()
df_merge.describe().round(4)
df_merge.isnull().sum()"""),
        ],
        "🧹 Preprocessing": [
            ("Drop Irrelevant Columns", """df_merge.drop(['Brand','Postcode','Phone_Number','Timezone'],
    axis=1, inplace=True)"""),
            ("Fix Serve_Size Column", """df_merge['Serve_Size'] = (df_merge['Serve_Size']
    .astype(str)
    .str.replace('[.\\d]+ oz ', '', regex=True)
    .str.replace('[\\d]+ cookie ', '', regex=True)
    .str.replace(' g', '', regex=False)
    .str.replace(' ml', '', regex=False)
)
df_merge['Serve_Size'] = df_merge['Serve_Size'].astype(float).astype(int)"""),
            ("Fix Sodium Missing Values", """df_merge['Sodium'] = df_merge.groupby('Category')['Sodium'].transform(
    lambda x: np.where(x == '-', np.nan, x)
).astype(float)

df_merge['Sodium'] = df_merge.groupby('Category')['Sodium'].transform(
    lambda x: x.fillna(x.median())
)"""),
            ("Fix Employee/Customer Decimals", """df_merge['Number_of_Employees'] = df_merge['Number_of_Employees'].apply(np.floor).astype(int)
df_merge['Customers'] = df_merge['Customers'].apply(np.floor).astype(int)"""),
            ("Round Financial Columns", """df_merge = df_merge.round(decimals=3)"""),
        ],
        "🏪 5.1 Outlet Metrics": [
            ("Ownership Type Distribution", """df_merge['Ownership_Type'].value_counts()

# Pie chart
df_merge['Ownership_Type'].value_counts().plot(
    kind='pie', explode=[0.05,0.05,0.05],
    autopct='%3.1f%%', figsize=(10,10),
    shadow=True, cmap='summer'
)"""),
            ("Top 10 Outlets by Revenue", """df_merge.nlargest(10, 'Revenue')[
    ['Store_Name','City','State','Revenue']
]"""),
            ("Top 10 Outlets by Profit", """df_merge.nlargest(10, 'Profits')[
    ['Store_Name','City','State','Profits']
]"""),
            ("Top 10 by Employee Count", """df_merge.nlargest(10, 'Number_of_Employees')[
    ['Store_Name','Number_of_Employees','City','Country']
]"""),
            ("Top 10 by Footfall", """df_merge.nlargest(10, 'Customers')[
    ['Store_Name','Country','Customers']
]"""),
        ],
        "🥗 5.2 Nutritional Analysis": [
            ("Menu Category Count", """df_merge.groupby('Category')['Best_Selling_Item'].count()\\
    .sort_values(ascending=False)\\
    .plot(kind='bar', color='g')"""),
            ("Avg Calories by Category", """df_merge.groupby('Category')['Energy'].median()\\
    .sort_values()\\
    .plot(kind='barh', figsize=(12,8), color='red')"""),
            ("Grilled vs Crispy Fat", """df_merge['Grilled'] = df_merge['Best_Selling_Item'].str.contains('Grilled')

crispy_names = df_merge.loc[df_merge.Grilled==True, 'Best_Selling_Item']\\
    .str.replace('Grilled', 'Crispy')

grilled_df = df_merge.loc[df_merge.Grilled==True, ['Best_Selling_Item','Total_Fat']]
crispy_df  = df_merge.loc[df_merge['Best_Selling_Item'].isin(crispy_names),
                           ['Best_Selling_Item','Total_Fat']]"""),
            ("Sugar by Category", """df_merge.groupby('Category')['Sugars'].mean()\\
    .sort_values(ascending=False)\\
    .plot(kind='bar', figsize=(15,8), color='orange')"""),
            ("Fibre Boxplot", """sns.boxplot(data=df_merge, x='Category', y='Dietary_Fibre',
    palette='viridis', width=0.8)
plt.xticks(rotation=90)"""),
            ("Nutritious vs Non-Nutritious Score", """df_merge['Nutritious']     = df_merge['Protein'] + df_merge['Dietary_Fibre']
df_merge['Non-Nutritious'] = (df_merge['Total_Fat'] + df_merge['Saturated_Fat']
                               + df_merge['Trans_Fat'] + df_merge['Cholestrol'])

# Heatmap for Breakfast category
df_n = (df_merge[df_merge['Category']=='Breakfast']
    .groupby('Best_Selling_Item').sum()
    .sort_values('Nutritious', ascending=False).head(10))
sns.heatmap(df_n[['Protein','Dietary_Fibre']], annot=True, cmap='viridis')"""),
            ("Most Protein-Rich Item", """df_merge.loc[df_merge['Protein'].idxmax(), 'Best_Selling_Item']
# → Chicken McNuggets (40 piece) — 87g protein"""),
        ],
        "🌍 5.3–5.7 Geography & Combined": [
            ("City Outlet Count", """df_merge['City'].value_counts()[:10]\\
    .plot(kind='bar', figsize=(15,7), color='red')"""),
            ("State Outlet Count", """df_merge['State'].value_counts()[:10]\\
    .plot(kind='barh', figsize=(15,7), color='black')"""),
            ("Revenue by Best-Seller Category", """df_merge.groupby('Category')['Revenue'].mean()\\
    .sort_values()\\
    .plot(kind='bar', figsize=(15,7), color='orange')"""),
            ("Ownership Type by Country", """sns.catplot(x='Ownership_Type', y='Number_of_Employees',
    hue='Country', data=df_merge, height=7,
    kind='bar', palette='spring')"""),
            ("Top 10 India + US by Revenue", """india_top10 = df_merge[df_merge['Country']=='IN']['Revenue']\\
    .sort_values(ascending=False)[:10].index

top10 = pd.concat([
    df_merge.iloc[india_top10, :],
    df_merge.nlargest(10, 'Revenue')
])"""),
            ("Avg Revenue by US State", """df_merge[df_merge['Country']=='US']\\
    .groupby('State')['Revenue'].mean()\\
    .sort_values(ascending=False)"""),
            ("India vs US Nutrition Comparison", """nutritional_cols = ['Energy','Protein','Sugars','Total_Fat',
    'Saturated_Fat','Cholestrol','Carbohydrates','Dietary_Fibre','Sodium']

for col in nutritional_cols:
    plt.figure(figsize=(15,5))
    df_merge[df_merge['Country']=='US'].groupby('Category')[col].mean()\\
        .plot(kind='bar', color='blue', alpha=0.7)
    df_merge[df_merge['Country']=='IN'].groupby('Category')[col].mean()\\
        .plot(kind='bar', color='red')
    plt.legend(['USA','India'])"""),
            ("Revenue by Country × Category (Pie)", """df_merge.groupby(['Country','Category'])['Revenue'].mean()\\
    .plot(kind='pie', autopct='%3.1f%%',
    wedgeprops=dict(width=0.15),
    figsize=(13,12), cmap='inferno')"""),
        ],
    }

    for section, items in queries.items():
        with st.expander(section, expanded=False):
            for title, code in items:
                st.markdown(f"**{title}**")
                st.code(code, language="python")
                st.markdown("---")
