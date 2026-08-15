# =========================================================
# JARVIS V7.6 - UNIFIED TOOL REGISTRY
# =========================================================

import asyncio

from mcp_tool_registry import MCPToolRegistry


class UnifiedToolRegistry:

    def __init__(self, mcp_server_script=None):

        self.native_tools = {}
        self.mcp_registry = None
        self.mcp_tools = {}

        if mcp_server_script:

            self.mcp_registry = MCPToolRegistry(
                mcp_server_script
            )

    # =====================================================
    # REGISTER NATIVE V3 TOOL
    # =====================================================

    def register_native_tool(
        self,
        name,
        description="",
        parameters=None,
        executor=None
    ):

        self.native_tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters or {
                "type": "object",
                "properties": {}
            },
            "source": "native",
            "executor": executor,
        }

    # =====================================================
    # DISCOVER MCP TOOLS
    # =====================================================

    async def discover_mcp_tools(self):

        if not self.mcp_registry:

            return []

        tools = await self.mcp_registry.discover()

        self.mcp_tools = {}

        for tool in tools:

            self.mcp_tools[
                tool["name"]
            ] = tool

        return tools

    # =====================================================
    # GET ALL TOOLS
    # =====================================================

    def get_all_tools(self):

        tools = []

        for tool in self.native_tools.values():

            public_tool = dict(tool)

            public_tool.pop(
                "executor",
                None
            )

            tools.append(
                public_tool
            )

        tools.extend(
            self.mcp_tools.values()
        )

        return tools

    # =====================================================
    # LOOKUP TOOL
    # =====================================================

    def get_tool(
        self,
        name
    ):

        if name in self.native_tools:

            return self.native_tools[name]

        if name in self.mcp_tools:

            return self.mcp_tools[name]

        return None

    # =====================================================
    # TOOL SOURCE
    # =====================================================

    def get_source(
        self,
        name
    ):

        tool = self.get_tool(
            name
        )

        if not tool:

            return None

        return tool.get(
            "source"
        )