# Formatting functions
def format_percentage(value, decimals=2):
    """Format decimal as percentage"""
    return f"{value * 100:.{decimals}f}%"

def format_currency(value, symbol="$"):
    """Format number as currency"""
    return f"{symbol}{value:,.2f}"

def determine_trend(current, previous):
    """Determine trend direction"""
    if current > previous:
        return "up"
    elif current < previous:
        return "down"
    return "stable"