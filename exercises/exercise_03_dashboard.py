"""
Exercise 3: Interactive Dashboard Creation (Bonus)

Learning Objectives:
- Create web-based data visualizations
- Build interactive dashboards with Dash/Plotly
- Deploy local web applications
- Connect data processing to user interfaces

Estimated Time: 20 minutes

Difficulty Levels:
- Basic: Create simple charts with Plotly
- Intermediate: Build Dash application layout
- Advanced: Add interactivity and callbacks
"""

# TODO 1: Import necessary libraries
# HINT: You'll need dash, plotly, pandas, and dash dependencies
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# TODO 2: Load and prepare data
def load_dashboard_data():
    """Load data for dashboard visualization"""
    # Your code here
    # Load historical trends
    # Load monthly data
    # Prepare data for charts
    pass

# TODO 3: Create individual charts (Basic)
def create_trend_chart(df):
    """Create line chart for historical trends"""
    # Your code here
    # Use plotly express or graph objects
    # Return figure object
    pass

def create_comparison_chart(df):
    """Create bar chart for indicator comparisons"""
    # Your code here
    # Return figure object
    pass

# TODO 4: Build Dash application layout (Intermediate)
def create_app_layout():
    """Create the dashboard layout"""
    # Your code here
    # Use html.Div, dcc.Graph, etc.
    # Include multiple charts
    # Add titles and descriptions
    pass

# TODO 5: Add interactivity with callbacks (Advanced)
def setup_callbacks(app):
    """Set up interactive callbacks"""
    # Your code here
    # @app.callback decorators
    # Update charts based on user input
    # Filter data dynamically
    pass

# TODO 6: Main dashboard application
def main():
    """Run the dashboard application"""
    # Your code here
    # Create app instance
    # Set up layout
    # Configure callbacks
    # Run server
    pass

if __name__ == "__main__":
    main()