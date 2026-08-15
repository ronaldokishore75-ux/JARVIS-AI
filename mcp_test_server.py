# =========================================================
# JARVIS V7.2 - MCP STDIO SERVER
# =========================================================

from mcp.server import MCPServer


mcp = MCPServer(
    "JARVIS Stdio Test Server"
)


@mcp.tool()
def hello_jarvis(
    name: str = "Kishore"
) -> str:
    """
    Return a simple greeting through MCP.
    """

    return (
        f"Hello {name}, "
        "MCP stdio is connected to JARVIS."
    )
@mcp.tool()
def get_jarvis_status() -> str:
    """
    Return a simple JARVIS status message.
    """

    return "JARVIS MCP server is online and ready."


if __name__ == "__main__":
    mcp.run()