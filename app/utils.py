"""
Utility functions for data processing and visualization in the Streamlit dashboard.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_cleaned_data(data_dir: str = "data") -> pd.DataFrame:
    """
    Load all cleaned country datasets and combine them.
    
    Args:
        data_dir: Directory containing the cleaned CSV files
        
    Returns:
        Combined DataFrame with all countries' data
    """
    # Handle both relative and absolute paths
    data_path = Path(data_dir)
    
    # If relative path doesn't exist, try from project root
    if not data_path.exists():
        # Try from current working directory (project root when running streamlit)
        project_root = Path.cwd()
        data_path = project_root / data_dir
        if not data_path.exists():
            # Try from app directory
            app_dir = Path(__file__).parent
            data_path = app_dir.parent / data_dir
    
    # Load cleaned datasets
    benin_df = pd.read_csv(data_path / "benin_clean.csv")
    sierra_leone_df = pd.read_csv(data_path / "sierra_leone_clean.csv")
    togo_df = pd.read_csv(data_path / "togo_clean.csv")
    
    # Convert Timestamp to datetime
    benin_df['Timestamp'] = pd.to_datetime(benin_df['Timestamp'])
    sierra_leone_df['Timestamp'] = pd.to_datetime(sierra_leone_df['Timestamp'])
    togo_df['Timestamp'] = pd.to_datetime(togo_df['Timestamp'])
    
    # Add country column for identification
    benin_df['Country'] = 'Benin'
    sierra_leone_df['Country'] = 'Sierra Leone'
    togo_df['Country'] = 'Togo'
    
    # Combine all datasets
    combined_df = pd.concat([benin_df, sierra_leone_df, togo_df], ignore_index=True)
    
    return combined_df


def filter_data_by_countries(df: pd.DataFrame, selected_countries: list) -> pd.DataFrame:
    """
    Filter DataFrame by selected countries.
    
    Args:
        df: Combined DataFrame
        selected_countries: List of country names to filter
        
    Returns:
        Filtered DataFrame
    """
    if not selected_countries:
        return df
    return df[df['Country'].isin(selected_countries)]


def filter_data_by_date_range(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    """
    Filter DataFrame by date range.
    
    Args:
        df: DataFrame with Timestamp column
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        Filtered DataFrame
    """
    return df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]


def get_summary_statistics(df: pd.DataFrame, metrics: list = ['GHI', 'DNI', 'DHI']) -> pd.DataFrame:
    """
    Calculate summary statistics for specified metrics by country.
    
    Args:
        df: DataFrame with country and metric columns
        metrics: List of metric columns to analyze
        
    Returns:
        DataFrame with summary statistics
    """
    summary_list = []
    
    for country in df['Country'].unique():
        country_df = df[df['Country'] == country]
        country_stats = {'Country': country}
        
        for metric in metrics:
            if metric in country_df.columns:
                values = country_df[metric].dropna()
                country_stats[f'{metric}_mean'] = values.mean()
                country_stats[f'{metric}_median'] = values.median()
                country_stats[f'{metric}_std'] = values.std()
                country_stats[f'{metric}_min'] = values.min()
                country_stats[f'{metric}_max'] = values.max()
        
        summary_list.append(country_stats)
    
    return pd.DataFrame(summary_list)


def create_boxplot(df: pd.DataFrame, metric: str, countries: list = None) -> go.Figure:
    """
    Create an interactive boxplot for a given metric.
    
    Args:
        df: DataFrame with data
        metric: Metric column to plot
        countries: List of countries to include (None for all)
        
    Returns:
        Plotly figure object
    """
    if countries:
        df = df[df['Country'].isin(countries)]
    
    fig = go.Figure()
    
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country][metric].dropna()
        fig.add_trace(go.Box(
            y=country_data,
            name=country,
            boxpoints='outliers',
            marker_color=px.colors.qualitative.Set2[list(df['Country'].unique()).index(country) % len(px.colors.qualitative.Set2)]
        ))
    
    fig.update_layout(
        title=f'{metric} Comparison by Country',
        yaxis_title=f'{metric} (W/m²)',
        xaxis_title='Country',
        showlegend=False,
        height=500,
        template='plotly_white'
    )
    
    return fig


def create_time_series_plot(df: pd.DataFrame, metric: str, countries: list = None, aggregation: str = 'daily') -> go.Figure:
    """
    Create an interactive time series plot for a given metric.
    
    Args:
        df: DataFrame with Timestamp and metric columns
        metric: Metric column to plot
        countries: List of countries to include (None for all)
        aggregation: Aggregation level ('hourly', 'daily', 'monthly')
        
    Returns:
        Plotly figure object
    """
    if countries:
        df = df[df['Country'].isin(countries)]
    
    # Set Timestamp as index for resampling
    df = df.set_index('Timestamp').sort_index()
    
    # Aggregate data
    if aggregation == 'hourly':
        resampled = df.groupby('Country').resample('H')[metric].mean().reset_index()
    elif aggregation == 'daily':
        resampled = df.groupby('Country').resample('D')[metric].mean().reset_index()
    elif aggregation == 'monthly':
        resampled = df.groupby('Country').resample('M')[metric].mean().reset_index()
    else:
        resampled = df.groupby('Country').resample('D')[metric].mean().reset_index()
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    for i, country in enumerate(resampled['Country'].unique()):
        country_data = resampled[resampled['Country'] == country]
        fig.add_trace(go.Scatter(
            x=country_data['Timestamp'],
            y=country_data[metric],
            name=country,
            mode='lines',
            line=dict(color=colors[i % len(colors)], width=2)
        ))
    
    fig.update_layout(
        title=f'{metric} Time Series ({aggregation.capitalize()} Average)',
        xaxis_title='Date',
        yaxis_title=f'{metric} (W/m²)',
        hovermode='x unified',
        height=500,
        template='plotly_white',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig


def create_country_ranking_bar(df: pd.DataFrame, metric: str = 'GHI') -> go.Figure:
    """
    Create a bar chart ranking countries by average metric value.
    
    Args:
        df: DataFrame with country and metric columns
        metric: Metric to rank by
        
    Returns:
        Plotly figure object
    """
    ranking = df.groupby('Country')[metric].mean().sort_values(ascending=False).reset_index()
    ranking.columns = ['Country', f'Average {metric}']
    
    fig = go.Figure(data=[
        go.Bar(
            x=ranking['Country'],
            y=ranking[f'Average {metric}'],
            marker_color=px.colors.qualitative.Set2[:len(ranking)],
            text=ranking[f'Average {metric}'].round(2),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f'Country Ranking by Average {metric}',
        xaxis_title='Country',
        yaxis_title=f'Average {metric} (W/m²)',
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def create_correlation_heatmap(df: pd.DataFrame, countries: list = None, metrics: list = None) -> go.Figure:
    """
    Create a correlation heatmap for specified metrics.
    
    Args:
        df: DataFrame with data
        countries: List of countries to include (None for all)
        metrics: List of metrics to correlate (None for default)
        
    Returns:
        Plotly figure object
    """
    if countries:
        df = df[df['Country'].isin(countries)]
    
    if metrics is None:
        metrics = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'TModA', 'TModB']
    
    # Filter to only include metrics that exist in the dataframe
    metrics = [m for m in metrics if m in df.columns]
    
    corr_matrix = df[metrics].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.round(2).values,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Correlation Heatmap',
        height=600,
        template='plotly_white'
    )
    
    return fig


def get_country_rankings_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a rankings table with key metrics for each country.
    
    Args:
        df: DataFrame with country and metric columns
        
    Returns:
        DataFrame with rankings
    """
    metrics = ['GHI', 'DNI', 'DHI']
    rankings = []
    
    for metric in metrics:
        if metric in df.columns:
            country_means = df.groupby('Country')[metric].mean().sort_values(ascending=False)
            for rank, (country, value) in enumerate(country_means.items(), 1):
                rankings.append({
                    'Metric': metric,
                    'Rank': rank,
                    'Country': country,
                    'Average Value': value,
                    'Unit': 'W/m²'
                })
    
    return pd.DataFrame(rankings)

