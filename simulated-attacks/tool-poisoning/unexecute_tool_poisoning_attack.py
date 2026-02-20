import os
from pathlib import Path

def restore_tool_poisoning():
    """Restore tool_poisoning.py to its original state."""
    original_content = '''"""Provides functionality for submitting issue tickets."""

from fastmcp import FastMCP
from typing import List

mcp = FastMCP("Ticketing Customer Support Agent")

@mcp.tool()
def create_ticket(
    title: str,
    description: str,
    notifyList: List[str]
) -> str:
    """
    Create a new IT support ticket in the system.
    """
    all_recipients = ["it.support@company.com"] + notifyList
    return (
    f"Ticket created: {title} - "
    f"Description: {description} - "
    f"Notifications sent to: {','.join(all_recipients)}"
)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
'''
    
    file_path = Path(__file__).parent / "tool_poisoning.py"
    file_path.write_text(original_content)
    print("tool_poisoning.py has been restored to its original state.")

if __name__ == "__main__":
    restore_tool_poisoning()