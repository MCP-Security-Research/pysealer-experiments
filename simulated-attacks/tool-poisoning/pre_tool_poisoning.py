"""Provides functionality for submitting issue tickets."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Ticketing Customer Support Agent")

@mcp.tool()
def create_ticket(
    title: str,
    description: str,
) -> str:
    """
    Create a new IT support ticket in the system.
    """
    return f"Ticket created: {title} - Description: {description}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
