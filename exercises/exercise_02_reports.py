"""
Exercise 2: Automated Report Generation

Learning Objectives:
- Process and analyze data programmatically
- Generate Excel reports with charts
- Create formatted Word documents using templates
- Build interactive dashboards
- Automate repetitive reporting tasks

Estimated Time: 20 minutes

Difficulty Levels:
- Basic: Load data and calculate basic metrics
- Intermediate: Generate Excel report with charts
- Advanced: Create Word document using template + Dashboard (Bonus)
"""

# TODO 1: Import necessary libraries
# HINT: You'll need pandas, openpyxl, python-docx, plotly, and os
import pandas as pd
import openpyxl
from openpyxl.chart import LineChart, Reference
from docx import Document
from docx.shared import Pt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# TODO 2: Load and process monthly data
def load_monthly_data(file_path='data/sample_monthly_data.csv'):
    """Load monthly statistics data"""
    # Your code here
    df = pd.read_csv(file_path)
    return df

# TODO 3: Calculate key metrics (Basic)
def calculate_metrics(df):
    """Calculate growth rates and trends"""
    # Your code here
    # Calculate year-over-year growth rates
    # Calculate rolling averages
    # Identify significant changes
    pass

# TODO 3.5: Generate insights from metrics
def generate_insights(df, metrics):
    """Generate rule-based insights from data and metrics"""
    # Your code here
    # Analyze trends and changes
    # Create meaningful insights
    # Return list of insight strings
    pass

# TODO 4: Generate Excel report with charts (Intermediate)
def generate_excel_report(df, output_file='output/monthly_report.xlsx'):
    """Create Excel report with data and charts"""
    # Your code here
    # Create workbook
    # Add data sheet
    # Add charts (line chart for trends)
    # Format the report
    pass

# TODO 5: Create Word document using template (Advanced)
def generate_word_report(metrics, insights, output_file='output/monthly_report.docx'):
    """Create formatted Word document using template"""
    # Your code here
    # Load the press release template
    # Replace placeholders with actual data
    # Add metrics and insights
    # Save the document
    pass

# TODO 6: Create interactive dashboard (Bonus)
def generate_dashboard(df, metrics, output_file='output/dashboard.html'):
    """Create an interactive dashboard with Plotly"""
    # Your code here
    # Import plotly libraries
    # Create charts for trends
    # Add interactive elements
    # Save as HTML file
    pass

# TODO 7: Main execution function
def main():
    """Main function to run the report generation"""
    # Your code here
    # Load data
    # Calculate metrics
    # Generate insights
    # Generate Excel report
    # Generate Word report using template
    # Generate dashboard (bonus)
    # Print success message
    pass

if __name__ == "__main__":
    main()
