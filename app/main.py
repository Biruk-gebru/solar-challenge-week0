"""
Streamlit Dashboard for Solar Data Analysis

This dashboard visualizes solar radiation data from Benin, Sierra Leone, and Togo
to help identify high-potential regions for solar installation.
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add parent directory to path to import utils
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import utils - try both methods for compatibility
try:
    from app.utils import (
        load_cleaned_data,
        filter_data_by_countries,
        filter_data_by_date_range,
        get_summary_statistics,
        create_boxplot,
        create_time_series_plot,
        create_country_ranking_bar,
        create_correlation_heatmap,
        get_country_rankings_table
    )
except ImportError:
    # Alternative import if running from app directory
    from utils import (
        load_cleaned_data,
        filter_data_by_countries,
        filter_data_by_date_range,
        get_summary_statistics,
        create_boxplot,
        create_time_series_plot,
        create_country_ranking_bar,
        create_correlation_heatmap,
        get_country_rankings_table
    )

# Page configuration
st.set_page_config(
    page_title="Solar Data Analysis Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">☀️ Solar Data Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        Analyzing solar radiation data from Benin, Sierra Leone, and Togo to identify 
        high-potential regions for solar installation
    </div>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load and cache the cleaned data."""
    try:
        data = load_cleaned_data(data_dir="data")
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure the cleaned CSV files are in the 'data' directory:")
        st.code("""
        data/
          ├── benin_clean.csv
          ├── sierra_leone_clean.csv
          └── togo_clean.csv
        """)
        return None

# Load data
with st.spinner("Loading data..."):
    df = load_data()

if df is None:
    st.stop()

# Sidebar for filters
st.sidebar.header("🔧 Filters & Controls")

# Country selection
available_countries = sorted(df['Country'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=available_countries,
    default=available_countries,
    help="Select one or more countries to analyze"
)

# Date range filter
st.sidebar.subheader("📅 Date Range")
min_date = df['Timestamp'].min().date()
max_date = df['Timestamp'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Filter data by date range"
)

# Metric selection for detailed analysis
st.sidebar.subheader("📊 Metrics")
available_metrics = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'TModA', 'TModB']
selected_metric = st.sidebar.selectbox(
    "Primary Metric",
    options=available_metrics,
    index=0,
    help="Select the primary metric for detailed analysis"
)

# Time series aggregation
st.sidebar.subheader("⏱️ Time Series Aggregation")
time_agg = st.sidebar.radio(
    "Aggregation Level",
    options=['hourly', 'daily', 'monthly'],
    index=1,
    help="Select the time aggregation level for time series plots"
)

# Filter data based on selections
filtered_df = filter_data_by_countries(df, selected_countries)

if len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])
    filtered_df = filter_data_by_date_range(filtered_df, start_date, end_date)

# Check if we have data after filtering
if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selections.")
    st.stop()

# Main dashboard content
# Key Metrics Overview
st.header("📈 Key Metrics Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_ghi = filtered_df.groupby('Country')['GHI'].mean().mean()
    st.metric("Average GHI", f"{avg_ghi:.2f} W/m²")

with col2:
    avg_dni = filtered_df.groupby('Country')['DNI'].mean().mean()
    st.metric("Average DNI", f"{avg_dni:.2f} W/m²")

with col3:
    avg_dhi = filtered_df.groupby('Country')['DHI'].mean().mean()
    st.metric("Average DHI", f"{avg_dhi:.2f} W/m²")

with col4:
    total_records = len(filtered_df)
    st.metric("Total Records", f"{total_records:,}")

# Country Ranking
st.header("🏆 Country Rankings")
ranking_metric = st.selectbox(
    "Rank by Metric",
    options=['GHI', 'DNI', 'DHI'],
    index=0,
    key='ranking_metric'
)

ranking_fig = create_country_ranking_bar(filtered_df, metric=ranking_metric)
st.plotly_chart(ranking_fig, use_container_width=True)

# Summary Statistics Table
st.header("📊 Summary Statistics")
summary_stats = get_summary_statistics(filtered_df, metrics=['GHI', 'DNI', 'DHI'])

# Format the summary statistics table for display
if not summary_stats.empty:
    # Create a more readable format
    display_stats = []
    for _, row in summary_stats.iterrows():
        country = row['Country']
        for metric in ['GHI', 'DNI', 'DHI']:
            if f'{metric}_mean' in row:
                display_stats.append({
                    'Country': country,
                    'Metric': metric,
                    'Mean': f"{row[f'{metric}_mean']:.2f}",
                    'Median': f"{row[f'{metric}_median']:.2f}",
                    'Std Dev': f"{row[f'{metric}_std']:.2f}",
                    'Min': f"{row[f'{metric}_min']:.2f}",
                    'Max': f"{row[f'{metric}_max']:.2f}"
                })
    
    stats_df = pd.DataFrame(display_stats)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    # Download button for summary statistics
    csv = stats_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Summary Statistics",
        data=csv,
        file_name="summary_statistics.csv",
        mime="text/csv"
    )

# Boxplots Comparison
st.header("📦 Distribution Comparison - Boxplots")
metric_tabs = st.tabs(['GHI', 'DNI', 'DHI'])

for i, metric in enumerate(['GHI', 'DNI', 'DHI']):
    with metric_tabs[i]:
        boxplot_fig = create_boxplot(filtered_df, metric, selected_countries)
        st.plotly_chart(boxplot_fig, use_container_width=True)
        
        # Add insights
        country_stats = filtered_df.groupby('Country')[metric].describe()
        st.subheader(f"{metric} Insights")
        for country in country_stats.index:
            mean_val = country_stats.loc[country, 'mean']
            median_val = country_stats.loc[country, '50%']
            st.write(f"**{country}**: Mean = {mean_val:.2f} W/m², Median = {median_val:.2f} W/m²")

# Time Series Analysis
st.header("⏱️ Time Series Analysis")
time_series_metric = st.selectbox(
    "Select Metric for Time Series",
    options=['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS'],
    index=0,
    key='time_series_metric'
)

time_series_fig = create_time_series_plot(
    filtered_df, 
    time_series_metric, 
    selected_countries, 
    aggregation=time_agg
)
st.plotly_chart(time_series_fig, use_container_width=True)

# Correlation Analysis
st.header("🔗 Correlation Analysis")
corr_metrics = st.multiselect(
    "Select Metrics for Correlation",
    options=available_metrics,
    default=['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'TModA', 'TModB'],
    key='corr_metrics'
)

if corr_metrics:
    corr_fig = create_correlation_heatmap(filtered_df, selected_countries, corr_metrics)
    st.plotly_chart(corr_fig, use_container_width=True)

# Detailed Rankings Table
st.header("📋 Detailed Rankings Table")
rankings_table = get_country_rankings_table(filtered_df)
if not rankings_table.empty:
    st.dataframe(rankings_table, use_container_width=True, hide_index=True)
    
    # Download button for rankings
    rankings_csv = rankings_table.to_csv(index=False)
    st.download_button(
        label="📥 Download Rankings Table",
        data=rankings_csv,
        file_name="country_rankings.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Solar Data Analysis Dashboard | MoonLight Energy Solutions</p>
        <p>Data from Benin, Sierra Leone, and Togo solar farms</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info("""
    This dashboard analyzes solar radiation data to identify 
    high-potential regions for solar installation.
    
    **Key Metrics:**
    - **GHI**: Global Horizontal Irradiance
    - **DNI**: Direct Normal Irradiance  
    - **DHI**: Diffuse Horizontal Irradiance
""")

st.sidebar.markdown("### 📝 Data Info")
st.sidebar.write(f"**Total Records**: {len(df):,}")
st.sidebar.write(f"**Date Range**: {df['Timestamp'].min().date()} to {df['Timestamp'].max().date()}")
st.sidebar.write(f"**Countries**: {', '.join(available_countries)}")

