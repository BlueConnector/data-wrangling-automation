"""
Exercise 3 Solution: Interactive Dashboard Creation (Bonus)
Complete implementation of a web-based dashboard using Dash/Plotly

This solution demonstrates:
1. Loading and preparing data for visualization
2. Creating interactive charts with Plotly
3. Building a Dash web application
4. Adding callbacks for interactivity
5. Deploying a local web dashboard
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import os


def load_dashboard_data():
    """
    Load and prepare data for dashboard visualization

    Returns:
        tuple: (monthly_data, historical_data)
    """
    try:
        # Load monthly data
        monthly_df = pd.read_csv('data/sample_monthly_data.csv')
        print(f"✓ Loaded monthly data: {len(monthly_df)} indicators")

        # Try to load historical data if available
        historical_path = 'data/historical_trends.csv'
        if os.path.exists(historical_path):
            historical_df = pd.read_csv(historical_path)
            print(f"✓ Loaded historical data: {len(historical_df)} records")
        else:
            historical_df = None
            print("ℹ Historical data not available - using monthly data only")

        return monthly_df, historical_df

    except FileNotFoundError as e:
        print(f"✗ Error loading data: {e}")
        return None, None


def create_trend_chart(df, indicator_name):
    """
    Create a line chart for a specific indicator

    Args:
        df: DataFrame with time series data
        indicator_name: Name of the indicator to chart

    Returns:
        plotly Figure object
    """
    if df is None:
        return None

    # Filter data for the specific indicator
    indicator_data = df[df['indicator_name'] == indicator_name].copy()

    if indicator_data.empty:
        return None

    # Create line chart
    fig = px.line(
        indicator_data,
        x='date',
        y='value',
        title=f'{indicator_name} Trend',
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode='x unified'
    )

    return fig


def create_comparison_chart(df):
    """
    Create a bar chart comparing current values across indicators

    Args:
        df: DataFrame with indicator data

    Returns:
        plotly Figure object
    """
    if df is None:
        return None

    # Get the most recent data for each indicator
    latest_data = df.sort_values('date').groupby('indicator_name').last().reset_index()

    fig = px.bar(
        latest_data,
        x='indicator_name',
        y='value',
        title='Current Indicator Values',
        color='indicator_name'
    )

    fig.update_layout(
        xaxis_title="Indicator",
        yaxis_title="Current Value",
        showlegend=False
    )

    return fig


def create_dashboard_app(monthly_df, historical_df):
    """
    Create and configure the Dash dashboard application

    Args:
        monthly_df: Monthly indicator data
        historical_df: Historical trend data (optional)

    Returns:
        Dash app object
    """
    app = Dash(__name__)

    # Get list of available indicators
    indicators = monthly_df['indicator_name'].unique() if monthly_df is not None else []

    app.layout = html.Div([
        html.H1('Economic Indicators Dashboard',
                style={'textAlign': 'center', 'marginBottom': 30}),

        html.Div([
            html.Label('Select Indicator:'),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=[{'label': ind, 'value': ind} for ind in indicators],
                value=indicators[0] if len(indicators) > 0 else None,
                style={'width': '50%'}
            )
        ], style={'marginBottom': 20}),

        html.Div([
            dcc.Graph(id='trend-chart'),
        ], style={'marginBottom': 30}),

        html.Div([
            dcc.Graph(id='comparison-chart'),
        ])
    ])

    @app.callback(
        Output('trend-chart', 'figure'),
        Input('indicator-dropdown', 'value')
    )
    def update_trend_chart(selected_indicator):
        """Update the trend chart based on selected indicator"""
        if selected_indicator and historical_df is not None:
            return create_trend_chart(historical_df, selected_indicator)
        elif selected_indicator and monthly_df is not None:
            # Create a simple chart from monthly data
            indicator_data = monthly_df[monthly_df['indicator_name'] == selected_indicator]
            fig = px.bar(
                indicator_data,
                x='date',
                y='value',
                title=f'{selected_indicator} (Monthly Data)'
            )
            return fig
        else:
            return {}

    @app.callback(
        Output('comparison-chart', 'figure'),
        Input('indicator-dropdown', 'value')
    )
    def update_comparison_chart(selected_indicator):
        """Update the comparison chart (static for now)"""
        return create_comparison_chart(monthly_df) or {}

    return app


def run_dashboard():
    """
    Load data and run the dashboard application
    """
    print("🚀 Starting Economic Indicators Dashboard...")

    # Load data
    monthly_df, historical_df = load_dashboard_data()

    if monthly_df is None:
        print("✗ No data available for dashboard")
        return

    # Create and run the app
    app = create_dashboard_app(monthly_df, historical_df)

    print("📊 Dashboard created successfully!")
    print("🌐 Open your browser to: http://127.0.0.1:8050/")
    print("💡 Use Ctrl+C to stop the server")

    app.run_server(debug=True)


if __name__ == "__main__":
    run_dashboard()