"""
Exercise 3: Interactive Dashboard Creation (Bonus) - COMPLETED EXAMPLE

This is a worked example showing all TODOs completed.
Students can reference this file if they get stuck on any step.

Learning Objectives:
- Create web-based data visualizations
- Build interactive dashboards with Dash/Plotly
- Deploy local web applications
- Connect data processing to user interfaces

Original file: exercise_03_dashboard.py
"""

# TODO 1: Import necessary libraries
# COMPLETED: Import Dash, Plotly, and pandas for dashboard creation
import dash
from dash import html, dcc, Input, Output, Dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os


# TODO 2: Load and prepare data
# COMPLETED: Load both monthly and historical data
def load_dashboard_data():
    """
    Load and prepare data for dashboard visualization.

    Returns:
        tuple: (monthly_df, historical_df) - both DataFrames ready for charting
    """
    try:
        # Load monthly data (current snapshot)
        monthly_df = pd.read_csv('data/sample_monthly_data.csv')
        print(f"Loaded monthly data: {len(monthly_df)} indicators")

        # Try to load historical data if available
        historical_path = 'data/historical_trends.csv'
        if os.path.exists(historical_path):
            historical_df = pd.read_csv(historical_path)

            # Create mapping from indicator codes to full names
            code_to_name = dict(zip(monthly_df['indicator_code'], monthly_df['indicator_name']))

            # Add indicator names to historical data
            historical_df['indicator_name'] = historical_df['indicator_code'].map(code_to_name)

            # Rename period to date for clarity
            historical_df = historical_df.rename(columns={'period': 'date'})

            print(f"Loaded historical data: {len(historical_df)} records")
        else:
            historical_df = None
            print("Historical data not available - using monthly data only")

        return monthly_df, historical_df

    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return None, None


# TODO 3: Create individual charts (Basic)
# COMPLETED: Create line chart for historical trends
def create_trend_chart(df, indicator_name):
    """
    Create a line chart for a specific indicator's historical trend.

    Args:
        df: Historical DataFrame with date and value columns
        indicator_name: Name of the indicator to chart

    Returns:
        Plotly Figure object
    """
    if df is None:
        return go.Figure()

    # Filter data for the specific indicator
    indicator_data = df[df['indicator_name'] == indicator_name].copy()

    if indicator_data.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text=f"No historical data available for {indicator_name}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#6c757d")
        )
        fig.update_layout(
            title=f'{indicator_name} Trend',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        return fig

    # Create line chart with markers
    fig = px.line(
        indicator_data,
        x='date',
        y='value',
        title=f'{indicator_name} Trend',
        markers=True
    )

    # Customize appearance
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode='x unified',
        template='plotly_white'
    )

    fig.update_traces(
        line=dict(color='#007bff', width=2),
        marker=dict(size=6)
    )

    return fig


# COMPLETED: Create bar chart for indicator comparisons
def create_comparison_chart(df):
    """
    Create a bar chart comparing all indicators' current values.

    Args:
        df: Monthly DataFrame with indicator data

    Returns:
        Plotly Figure object
    """
    if df is None:
        return go.Figure()

    # Create bar chart
    fig = px.bar(
        df,
        x='indicator_code',
        y='value',
        title='Current Values by Indicator',
        color='value',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        xaxis_title="Indicator",
        yaxis_title="Value",
        showlegend=False,
        template='plotly_white'
    )

    return fig


# COMPLETED: Create indicator cards showing current values
def create_indicator_cards(df, selected_indicator=None):
    """
    Create indicator cards showing current values and month-over-month changes.

    Args:
        df: DataFrame with indicator data
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
            arrow = '+' if change > 0 else '' if change < 0 else ''
            change_text = f"{arrow}{change:,.1f} ({change_pct:+.1f}%)"
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

        # Create card
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
            html.Div("vs. previous month", style={
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


# TODO 4: Build Dash application layout (Intermediate)
# COMPLETED: Create the full dashboard layout
def create_app_layout(monthly_df, historical_df):
    """
    Create the dashboard layout with all components.

    Args:
        monthly_df: Monthly data DataFrame
        historical_df: Historical data DataFrame

    Returns:
        Dash layout (html.Div)
    """
    # Get list of available indicators
    indicators = monthly_df['indicator_name'].unique() if monthly_df is not None else []

    layout = html.Div([
        # Header
        html.H1('Economic Indicators Dashboard',
                style={'textAlign': 'center', 'marginBottom': '10px', 'color': '#333'}),

        html.P('Interactive visualization of key economic metrics',
               style={'textAlign': 'center', 'color': '#666', 'marginBottom': '30px'}),

        # Indicator selector
        html.Div([
            html.Label('Select Indicator:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=[{'label': ind, 'value': ind} for ind in indicators],
                value=indicators[0] if len(indicators) > 0 else None,
                style={'width': '50%'}
            )
        ], style={'marginBottom': '20px'}),

        # Trend chart
        html.Div([
            dcc.Graph(id='trend-chart'),
        ], style={'marginBottom': '30px'}),

        # Current indicator values section
        html.H3('Current Indicator Values', style={'marginBottom': '15px'}),

        html.Div(
            id='indicator-cards',
            style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'gap': '15px',
                'justifyContent': 'flex-start'
            }
        ),

        # Footer
        html.Hr(style={'marginTop': '40px'}),
        html.P(
            'Data source: sample_monthly_data.csv and historical_trends.csv',
            style={'textAlign': 'center', 'color': '#999', 'fontSize': '12px'}
        )
    ], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})

    return layout


# TODO 5: Add interactivity with callbacks (Advanced)
# COMPLETED: Set up callbacks for interactive updates
def setup_callbacks(app, monthly_df, historical_df):
    """
    Set up interactive callbacks to update charts based on user input.

    Args:
        app: Dash application instance
        monthly_df: Monthly data DataFrame
        historical_df: Historical data DataFrame
    """

    @app.callback(
        Output('trend-chart', 'figure'),
        Input('indicator-dropdown', 'value')
    )
    def update_trend_chart(selected_indicator):
        """Update the trend chart based on selected indicator."""
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
                height=400
            )
            return fig

        return go.Figure()

    @app.callback(
        Output('indicator-cards', 'children'),
        Input('indicator-dropdown', 'value')
    )
    def update_indicator_cards(selected_indicator):
        """Update indicator cards with highlighted selection."""
        return create_indicator_cards(monthly_df, selected_indicator)


# TODO 6: Main dashboard application
# COMPLETED: Create and run the complete dashboard
def main():
    """
    Run the dashboard application.
    """
    print("=" * 60)
    print("EXERCISE 3: INTERACTIVE DASHBOARD")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    monthly_df, historical_df = load_dashboard_data()

    if monthly_df is None:
        print("No data available for dashboard")
        return

    # Create Dash app
    print("\nCreating dashboard...")
    app = Dash(__name__)

    # Set up layout
    app.layout = create_app_layout(monthly_df, historical_df)

    # Set up callbacks
    setup_callbacks(app, monthly_df, historical_df)

    print("\nDashboard created successfully!")
    print("-" * 60)
    print("Open your browser to: http://127.0.0.1:8050/")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)

    # Run the server
    app.run(debug=True)


if __name__ == "__main__":
    main()
