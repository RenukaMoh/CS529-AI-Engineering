# Custom MCP servers Demo

# Import FastMCP to quickly create and run lightweight MCP servers
from mcp.server.fastmcp import FastMCP

# Import datetime to work with dates
from datetime import datetime

# Create an instance of FastMCP
mcp = FastMCP("My MCP Server")

# Tool 1 - Calculate the days between Dates
@mcp.tool()
def days_between(start_date: str, end_date: str) -> str:
    """
    Calculates the number of days between two dates.
    Expected format: YYYY-MM-DD
    Example: days_between("2025-02-15", "2025-03-01")
    """
    try:
        # Convert strings to datetime objects
        d1 = datetime.strptime(start_date, "%Y-%m-%d")
        d2 = datetime.strptime(end_date, "%Y-%m-%d")

        # Calculate absolute difference
        diff = abs((d2 - d1).days)

        return f"Number of days between {start_date} and {end_date}: {diff} days"
    
    except ValueError:
        return (
            "Invalid date format. Please use YYYY-MM-DD.\n"
            "Example: 2025-02-15"
        )

# Tool 2 - Calculate Increase/Desreased Percentage
@mcp.tool()
def percentage_change(old_value: float, new_value: float) -> str:
    """
    Calculate percentage increase or decrease from old_value to new_value.

    Example:
        percentage_change(80, 100)  -> 25.0% increase
        percentage_change(100, 80)  -> 20.0% decrease
    """
    if old_value == 0:
        return "Error: old_value cannot be 0 when calculating percentage change."

    change = new_value - old_value
    percent = (change / old_value) * 100
    # Conditional Operator Python syntax
    direction = "increase" if percent > 0 else "decrease" if percent < 0 else "no change"
    return (
        f"Old value: {old_value}, New value: {new_value}\n"
        f"Change: {percent:.2f}% ({direction})."
    )

# run the server
if __name__ == "__main__": 
    mcp.run()
    