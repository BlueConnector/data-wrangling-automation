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
            # Create mapping from indicator codes to full names using monthly data
            code_to_name = dict(zip(monthly_df['indicator_code'], monthly_df['indicator_name']))
            # Map codes to full names and rename columns
            historical_df['indicator_name'] = historical_df['indicator_code'].map(code_to_name)
            historical_df = historical_df.rename(columns={'period': 'date'})
            historical_df = historical_df.drop(columns=['indicator_code'])
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


def create_indicator_cards(df, selected_indicator=None):
    """
    Create indicator cards showing current values and month-over-month changes

    Args:
        df: DataFrame with indicator data (must have indicator_name, value, unit, previous_month_value)
        selected_indicator: Optional indicator to highlight

    Returns:
        List of Dash html components (cards)
    """
    if df is None:
        return []

    cards = []
    for _, row in df.iterrows():
        indicator_name = row['indicator_name']
        value = row['value']
        unit = row['unit']
        prev_value = row['previous_month_value']

        # Calculate month-over-month change
        if prev_value and prev_value != 0:
            change = value - prev_value
            change_pct = (change / prev_value) * 100

            # For unemployment, lower is better (invert color logic)
            is_unemployment = 'unemployment' in indicator_name.lower()
            if is_unemployment:
                is_positive = change < 0
            else:
                is_positive = change > 0

            change_color = '#28a745' if is_positive else '#dc3545'
            arrow = '▲' if change > 0 else '▼' if change < 0 else ''
            change_text = f"{arrow} {abs(change):,.1f} ({abs(change_pct):.1f}%)"
        else:
            change_text = "N/A"
            change_color = '#6c757d'

        # Format value based on unit
        if unit == 'millions':
            formatted_value = f"${value:,.0f}M"
        elif unit == 'percentage':
            formatted_value = f"{value:.1f}%"
        elif unit == 'index':
            formatted_value = f"{value:.1f}"
        elif unit == 'dollars':
            formatted_value = f"${value:,.0f}"
        elif unit == 'units':
            formatted_value = f"{value:,.0f}"
        else:
            formatted_value = f"{value:,.1f}"

        # Highlight selected indicator
        is_selected = indicator_name == selected_indicator
        border_color = '#007bff' if is_selected else '#dee2e6'
        border_width = '3px' if is_selected else '1px'
        background = '#f8f9ff' if is_selected else '#ffffff'

        card = html.Div([
            html.H4(indicator_name, style={
                'margin': '0 0 10px 0',
                'fontSize': '14px',
                'color': '#495057'
            }),
            html.Div(formatted_value, style={
                'fontSize': '24px',
                'fontWeight': 'bold',
                'color': '#212529'
            }),
            html.Div(change_text, style={
                'fontSize': '14px',
                'color': change_color,
                'marginTop': '5px'
            }),
            html.Div(f"vs. previous month", style={
                'fontSize': '11px',
                'color': '#6c757d'
            })
        ], style={
            'padding': '15px',
            'border': f'{border_width} solid {border_color}',
            'borderRadius': '8px',
            'backgroundColor': background,
            'textAlign': 'center',
            'minWidth': '180px'
        })

        cards.append(card)

    return cards


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

        html.H3('Current Indicator Values', style={'marginBottom': 15}),
        html.Div(
            id='indicator-cards',
            style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'gap': '15px',
                'justifyContent': 'flex-start'
            }
        )
    ])

    @app.callback(
        Output('trend-chart', 'figure'),
        Input('indicator-dropdown', 'value')
    )
    def update_trend_chart(selected_indicator):
        """Update the trend chart based on selected indicator"""
        if selected_indicator and historical_df is not None:
            fig = create_trend_chart(historical_df, selected_indicator)
            if fig is not None:
                return fig

        # No historical data available - show message
        if selected_indicator:
            fig = go.Figure()
            fig.add_annotation(
                text=f"No historical trend data available for {selected_indicator}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#6c757d")
            )
            fig.update_layout(
                title=f'{selected_indicator} Trend',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                height=300
            )
            return fig
        return {}

    @app.callback(
        Output('indicator-cards', 'children'),
        Input('indicator-dropdown', 'value')
    )
    def update_indicator_cards(selected_indicator):
        """Update indicator cards with highlighted selection"""
        return create_indicator_cards(monthly_df, selected_indicator)

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

    app.run(debug=True)


if __name__ == "__main__":
    run_dashboard()