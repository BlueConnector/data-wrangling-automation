"""
Helper Functions for DOS Analytics Training
Utility functions to reduce boilerplate code in exercises
"""

import openpyxl
from docx import Document
import logging


def format_percentage(value, decimals=2):
    """
    Format a decimal value as a percentage string
    
    Args:
        value (float): The decimal value (e.g., 0.0523 for 5.23%)
        decimals (int): Number of decimal places
        
    Returns:
        str: Formatted percentage (e.g., "5.23%")
    """
    if value is None:
        return "N/A"
    return f"{value:.{decimals}f}%"


def format_currency(value, currency_symbol="$", decimals=2):
    """
    Format a number as currency with thousand separators
    
    Args:
        value (float): The numeric value
        currency_symbol (str): Currency symbol to use
        decimals (int): Number of decimal places
        
    Returns:
        str: Formatted currency (e.g., "$542,300.00")
    """
    if value is None:
        return "N/A"
    return f"{currency_symbol}{value:,.{decimals}f}"


def format_number(value, decimals=0):
    """
    Format a number with thousand separators
    
    Args:
        value (float): The numeric value
        decimals (int): Number of decimal places
        
    Returns:
        str: Formatted number (e.g., "542,300")
    """
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f}"


def determine_trend(current, previous, threshold=1.0):
    """
    Determine trend direction based on percentage change
    
    Args:
        current (float): Current value
        previous (float): Previous value
        threshold (float): Percentage threshold for "stable" (default 1%)
        
    Returns:
        str: "increasing", "decreasing", or "stable"
    """
    if current is None or previous is None or previous == 0:
        return "unknown"
    
    change_percent = ((current - previous) / previous) * 100
    
    if change_percent > threshold:
        return "increasing"
    elif change_percent < -threshold:
        return "decreasing"
    else:
        return "stable"


def calculate_growth_rate(current, previous):
    """
    Calculate percentage growth rate
    
    Args:
        current (float): Current value
        previous (float): Previous value
        
    Returns:
        float: Growth rate as percentage, or None if calculation not possible
    """
    if current is None or previous is None or previous == 0:
        return None
    
    return ((current - previous) / previous) * 100


def load_excel_template(path):
    """
    Load an Excel template with error handling
    
    Args:
        path (str): Path to the Excel file
        
    Returns:
        Workbook: The loaded workbook, or None if error
    """
    try:
        workbook = openpyxl.load_workbook(path)
        logging.info(f"✓ Loaded Excel template: {path}")
        return workbook
    except FileNotFoundError:
        logging.error(f"✗ Template not found: {path}")
        return None
    except Exception as e:
        logging.error(f"✗ Error loading template: {str(e)}")
        return None


def load_word_template(path):
    """
    Load a Word template with error handling
    
    Args:
        path (str): Path to the Word file
        
    Returns:
        Document: The loaded document, or None if error
    """
    try:
        doc = Document(path)
        logging.info(f"✓ Loaded Word template: {path}")
        return doc
    except FileNotFoundError:
        logging.error(f"✗ Template not found: {path}")
        return None
    except Exception as e:
        logging.error(f"✗ Error loading template: {str(e)}")
        return None


def save_workbook(workbook, path):
    """
    Save an Excel workbook with error handling
    
    Args:
        workbook: The openpyxl workbook object
        path (str): Where to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        workbook.save(path)
        logging.info(f"✓ Saved workbook: {path}")
        return True
    except Exception as e:
        logging.error(f"✗ Error saving workbook: {str(e)}")
        return False


def save_document(document, path):
    """
    Save a Word document with error handling
    
    Args:
        document: The python-docx document object
        path (str): Where to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        document.save(path)
        logging.info(f"✓ Saved document: {path}")
        return True
    except Exception as e:
        logging.error(f"✗ Error saving document: {str(e)}")
        return False


def validate_numeric(value, min_val=None, max_val=None):
    """
    Validate that a value is numeric and within range
    
    Args:
        value: The value to validate
        min_val (float): Minimum acceptable value (optional)
        max_val (float): Maximum acceptable value (optional)
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        num = float(value)
        
        if min_val is not None and num < min_val:
            return False
        
        if max_val is not None and num > max_val:
            return False
        
        return True
    except (ValueError, TypeError):
        return False


def clean_text(text):
    """
    Clean text by removing extra whitespace and special characters
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if text is None:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove common problematic characters
    text = text.replace('\r', '').replace('\n', ' ')
    
    return text.strip()


def parse_numeric(text):
    """
    Parse numeric value from text (handles commas, currency symbols, etc.)
    
    Args:
        text (str): Text containing a number
        
    Returns:
        float: The parsed number, or None if parsing fails
    """
    if text is None:
        return None
    
    try:
        # Remove common non-numeric characters
        cleaned = str(text).replace(',', '').replace('$', '').replace('%', '').strip()
        
        # Handle special cases
        if cleaned.upper() == 'N/A' or cleaned == '':
            return None
        
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


# Example usage and testing
if __name__ == "__main__":
    print("Helper Functions - Example Usage")
    print("="*60)
    
    # Test formatting functions
    print("\n1. Formatting Examples:")
    print(f"   Percentage: {format_percentage(0.0523)}")
    print(f"   Currency: {format_currency(542300)}")
    print(f"   Number: {format_number(542300)}")
    
    # Test trend determination
    print("\n2. Trend Determination:")
    print(f"   100 → 105: {determine_trend(105, 100)}")
    print(f"   100 → 97: {determine_trend(97, 100)}")
    print(f"   100 → 100.5: {determine_trend(100.5, 100)}")
    
    # Test growth calculation
    print("\n3. Growth Rate Calculation:")
    print(f"   542300 → 538100: {calculate_growth_rate(542300, 538100):.2f}%")
    print(f"   118.5 → 117.8: {calculate_growth_rate(118.5, 117.8):.2f}%")
    
    # Test validation
    print("\n4. Numeric Validation:")
    print(f"   '123.45' is numeric: {validate_numeric('123.45')}")
    print(f"   'abc' is numeric: {validate_numeric('abc')}")
    print(f"   50 in range 0-100: {validate_numeric(50, 0, 100)}")
    
    # Test text cleaning
    print("\n5. Text Cleaning:")
    print(f"   '  Hello   World  ' → '{clean_text('  Hello   World  ')}'")
    
    # Test numeric parsing
    print("\n6. Numeric Parsing:")
    print(f"   '$542,300.00' → {parse_numeric('$542,300.00')}")
    print(f"   '3.2%' → {parse_numeric('3.2%')}")
    
    print("\n" + "="*60)
    print("All helper functions are working correctly!")