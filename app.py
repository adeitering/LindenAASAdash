import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import base64
import datetime
from fpdf import FPDF

# Load the data
df = pd.read_csv("linden_aasa_dashboard_data.csv")

st.set_page_config(page_title="Linden AASA Dashboard", layout="wide")

# Custom Styling for Linden Colors
green = "#145A32"
gold = "#B7950B"

# Guidance Section
st.markdown(f"""
    <style>
    body {{
        background-color: #FDFEFE !important;
    }}
    .main-title {{
        font-size: 40px;
        font-weight: bold;
        color: {green};
        text-align: center;
        margin-bottom: 5px;
    }}
    .subtitle {{
        font-size: 20px;
        color: {gold};
        text-align: center;
        margin-bottom: 25px;
    }}
    </style>
    <div class='main-title'>Linden Elementary AASA Performance Dashboard</div>
    <div class='subtitle'>Tracking Growth • Celebrating Success • Driving Instruction</div>
""", unsafe_allow_html=True)

with st.expander("🧭 How to Use This Dashboard Effectively", expanded=False):
    st.markdown("""
    This dashboard is a tool to guide conversations. We encourage:
    - Celebrating **growth** across years and content areas
    - Identifying **trends and needs** for targeted support
    - Supporting **cohort analysis** over time
    - Making **data-informed decisions** for instruction and intervention

    💬 Use this in PLCs, staff meetings, and one-on-ones with a mindset of **collective efficacy**.
    """)

# Horizontal filters
col1, col2, col3 = st.columns(3)
grade_filter = col1.multiselect("Select Grade(s)", sorted(df["Grade"].unique()), default=sorted(df["Grade"].unique()))
subject_filter = col2.multiselect("Select Subject(s)", sorted(df["Subject"].unique()), default=sorted(df["Subject"].unique()))
year_filter = col3.multiselect("Select Year(s)", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

# Filter data
df_filtered = df[(df["Grade"].isin(grade_filter)) &
                 (df["Subject"].isin(subject_filter)) &
                 (df["Year"].isin(year_filter))]

# Melt the data for plotting
df_melted = df_filtered.melt(id_vars=["Grade", "Subject", "Year"],
                             value_vars=["Level 1", "Level 2", "Level 3", "Level 4"],
                             var_name="Performance Level",
                             value_name="Percentage")
df_melted["hover"] = df_melted.apply(lambda row: f"{row['Grade']} {row['Subject']} {row['Year']}\n{row['Performance Level']}: {row['Percentage']:.1f}%", axis=1)

color_map = {
    "Level 1": "#e74c3c",
    "Level 2": "#f39c12",
    "Level 3": "#27ae60",
    "Level 4": "#2980b9"
}

# Side-by-side charts
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Performance Level Distribution")
    fig_bar = px.bar(df_melted,
                     x="Year",
                     y="Percentage",
                     color="Performance Level",
                     barmode="stack",
                     text=df_melted["Percentage"].round(1),
                     hover_name="hover",
                     facet_col="Grade", facet_col_spacing=0.08,
                     facet_row="Subject",
                     color_discrete_map=color_map)
    fig_bar.update_layout(yaxis=dict(title="% of Students", gridcolor="#ECECEC"),
                          plot_bgcolor="#FFFFFF")
    st.plotly_chart(fig_bar, use_container_width=True)
    # PNG download removed due to Streamlit Cloud limitations

with col_b:
    st.subheader("📈 Performance Trend by Level")
    fig_line = px.line(df_melted,
                       x="Year",
                       y="Percentage",
                       color="Performance Level",
                       line_group="Grade",
                       markers=True,
                       hover_name="hover",
                       facet_row="Subject",
                       color_discrete_map=color_map)
    fig_line.update_layout(yaxis=dict(title="% of Students", gridcolor="#ECECEC"),
                           plot_bgcolor="#FFFFFF")
    st.plotly_chart(fig_line, use_container_width=True)
    # PNG download removed due to Streamlit Cloud limitations

# PDF Report temporarily removed due to rendering issues

# Thank you footer
st.markdown("---")
st.markdown("**Data empowers us to grow. Thank you for being part of the journey.**")
