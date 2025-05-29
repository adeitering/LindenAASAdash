import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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

# Horizontal filters
col1, col2, col3 = st.columns(3)
grade_filter = col1.selectbox("Select Grade", sorted(df["Grade"].unique()))
subject_filter = col2.selectbox("Select Subject", sorted(df["Subject"].unique()))
year_filter = col3.multiselect("Select Year(s)", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

# Filter data
df_filtered = df[(df["Grade"] == grade_filter) &
                 (df["Subject"] == subject_filter) &
                 (df["Year"].isin(year_filter))]

# Melt the data for stacked bar plotting
df_melted = df_filtered.melt(id_vars=["Grade", "Subject", "Year"],
                             value_vars=["Level 1", "Level 2", "Level 3", "Level 4"],
                             var_name="Performance Level",
                             value_name="Percentage")

# Add hover text
df_melted["hover"] = df_melted.apply(lambda row: f"{row['Performance Level']}: {row['Percentage']:.1f}%", axis=1)

color_map = {
    "Level 1": "#e74c3c",
    "Level 2": "#f39c12",
    "Level 3": "#27ae60",
    "Level 4": "#2980b9"
}

# Layout: Side-by-side charts
col_a, col_b = st.columns(2)

with col_a:
    st.subheader(f"Performance Level Distribution - {grade_filter} {subject_filter}")
    fig_bar = px.bar(df_melted,
                     x="Year",
                     y="Percentage",
                     color="Performance Level",
                     color_discrete_map=color_map,
                     barmode="stack",
                     text=df_melted["Percentage"].round(1),
                     hover_name="hover")
    fig_bar.update_layout(yaxis=dict(title="% of Students", gridcolor="#ECECEC"),
                          xaxis=dict(type='category'),
                          plot_bgcolor="#FFFFFF")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    st.subheader("📈 Performance Trend by Level")
    fig_line = px.line(df_melted,
                       x="Year",
                       y="Percentage",
                       color="Performance Level",
                       markers=True,
                       color_discrete_map=color_map,
                       hover_name="hover")
    fig_line.update_layout(yaxis=dict(title="% of Students", gridcolor="#ECECEC"),
                           xaxis=dict(type='category'),
                           plot_bgcolor="#FFFFFF")
    st.plotly_chart(fig_line, use_container_width=True)

# Summary Table
st.subheader("📋 Data Table")
st.dataframe(df_filtered.set_index("Year"), use_container_width=True)

# Narrative Summary
if len(year_filter) == 1:
    year = year_filter[0]
    total_prof = df_filtered[df_filtered["Year"] == year]["Level 3"].values[0] + df_filtered[df_filtered["Year"] == year]["Level 4"].values[0]
    st.markdown(f"**In {year}, {total_prof:.1f}% of {grade_filter} students were Proficient or above in {subject_filter}.**")

# Download button
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Filtered Data as CSV",
                   data=csv,
                   file_name=f"{grade_filter}_{subject_filter}_data.csv",
                   mime='text/csv')

# Thank you footer
st.markdown("---")
st.markdown("**Data empowers us to grow. Thank you for being part of the journey.**")
