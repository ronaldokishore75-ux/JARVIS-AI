# =========================================================
# JARVIS V7.4 - MCP TOOL REGISTRY ADAPTER
# =========================================================

from mcp_client import MCPClient


class MCPToolRegistry:

    def __init__(self, server_script):
        self.server_script = server_script
        self.tools = {}

    # =====================================================
    # DISCOVER MCP TOOLS
    # =====================================================

    async def discover(self):

        client = MCPClient(
            self.server_script
        )

        discovered = await client.discover_tools()

        self.tools = {}

        for tool in discovered:

            normalized = self._normalize_tool(
                tool
            )

            self.tools[
                normalized["name"]
            ] = normalized

        return list(
            self.tools.values()
        )

    # =====================================================
    # NORMALIZE MCP TOOL
    # =====================================================

    def _normalize_tool(self, tool):

        return {
            "name": tool["name"],

            "description": (
                tool.get(
                    "description",
                    ""
                )
            ),

            "parameters": (
                tool.get(
                    "input_schema",
                    {
                        "type": "object",
                        "properties": {},
                    }
                )
            ),

            "source": "mcp",
        }

    # =====================================================
    # GET TOOL
    # =====================================================

    def get_tool(self, name):

        return self.tools.get(
            name
        )

    # =====================================================
    # GET ALL TOOLS
    # =====================================================

    def get_tools(self):

        return list(
            self.tools.values()
        )