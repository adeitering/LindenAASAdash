import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("linden_aasa_dashboard_data.csv")

st.set_page_config(page_title="Linden AASA Dashboard", layout="wide")

# Custom Styling for Linden Colors
green = "#145A32"
gold = "#B7950B"

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
    .stSidebar {{
        background-color: #F7F9F9;
    }}
    .css-18e3th9 {{
        padding: 2rem 1rem;
        background-color: #FFFFFF;
    }}
    </style>
    <div class='main-title'>Linden Elementary AASA Performance Dashboard</div>
    <div class='subtitle'>Tracking Growth • Celebrating Success • Driving Instruction</div>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Data")
    grade_filter = st.selectbox("Select Grade", sorted(df["Grade"].unique()))
    subject_filter = st.selectbox("Select Subject", sorted(df["Subject"].unique()))
    year_filter = st.multiselect("Select Year(s)", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

# Filter data
df_filtered = df[(df["Grade"] == grade_filter) &
                 (df["Subject"] == subject_filter) &
                 (df["Year"].isin(year_filter))]

# Melt the data for stacked bar plotting
df_melted = df_filtered.melt(id_vars=["Grade", "Subject", "Year"],
                             value_vars=["Level 1", "Level 2", "Level 3", "Level 4"],
                             var_name="Performance Level",
                             value_name="Percentage")

color_map = {
    "Level 1": "#e74c3c",  # Red
    "Level 2": "#f39c12",  # Orange
    "Level 3": "#27ae60",  # Green
    "Level 4": "#2980b9"   # Blue
}

# Bar chart
st.subheader(f"Performance Level Distribution - {grade_filter} {subject_filter}")
fig_bar = px.bar(df_melted,
                 x="Year",
                 y="Percentage",
                 color="Performance Level",
                 color_discrete_map=color_map,
                 barmode="stack",
                 text="Percentage")
fig_bar.update_layout(yaxis=dict(title="% of Students"), xaxis=dict(type='category'))
st.plotly_chart(fig_bar, use_container_width=True)

# Line chart for trends
st.subheader("📈 Performance Trend by Level")
fig_line = px.line(df_melted,
                   x="Year",
                   y="Percentage",
                   color="Performance Level",
                   markers=True,
                   color_discrete_map=color_map)
fig_line.update_layout(yaxis=dict(title="% of Students"), xaxis=dict(type='category'))
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.markdown("Dashboard created by Linden Elementary School to analyze AASA results for Grades 3–5 in ELA and Math.")
