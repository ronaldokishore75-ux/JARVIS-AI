# =========================================================
# JARVIS V7.3 - MCP CLIENT
# =========================================================

import sys

from mcp import Client
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:

    def __init__(self, server_script):
        self.server_script = server_script

    # =====================================================
    # SERVER PARAMETERS
    # =====================================================

    def _server_params(self):

        return StdioServerParameters(
            command=sys.executable,
            args=[
                self.server_script
            ],
        )

    # =====================================================
    # DISCOVER TOOLS
    # =====================================================

    async def discover_tools(self):

        server_params = self._server_params()

        async with Client(
            stdio_client(server_params)
        ) as client:

            result = await client.list_tools()

            tools = []

            for tool in result.tools:

                tools.append(
                    {
                        "name": tool.name,
                        "title": getattr(
                            tool,
                            "title",
                            None
                        ),
                        "description": (
                            tool.description or ""
                        ),
                        "input_schema": (
                            tool.input_schema
                        ),
                        "output_schema": getattr(
                            tool,
                            "output_schema",
                            None
                        ),
                    }
                )

            return tools

    # =====================================================
    # CALL TOOL
    # =====================================================

    async def call_tool(
        self,
        tool_name,
        arguments=None
    ):

        server_params = self._server_params()

        async with Client(
            stdio_client(server_params)
        ) as client:

            result = await client.call_tool(
                tool_name,
                arguments or {}
            )

            return result