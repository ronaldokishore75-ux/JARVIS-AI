# =========================================================
# JARVIS V7.7 - UNIFIED TOOL EXECUTOR
# =========================================================

from mcp_tool_executor import MCPToolExecutor


class UnifiedToolExecutor:

    def __init__(self, mcp_server_script=None):

        self.mcp_executor = None

        if mcp_server_script:

            self.mcp_executor = MCPToolExecutor(
                mcp_server_script
            )

    # =====================================================
    # EXECUTE TOOL
    # =====================================================

    async def execute(
        self,
        tool,
        arguments=None
    ):

        if not tool:

            return {
                "success": False,
                "error": "Tool not found."
            }

        arguments = arguments or {}

        tool_name = tool.get(
            "name"
        )

        source = tool.get(
            "source"
        )

        # =================================================
        # MCP TOOL
        # =================================================

        if source == "mcp":

            if not self.mcp_executor:

                return {
                    "success": False,
                    "tool": tool_name,
                    "error": (
                        "MCP executor is not configured."
                    )
                }

            return await self.mcp_executor.execute(
                tool_name,
                arguments
            )

        # =================================================
        # NATIVE V3 TOOL
        # =================================================

        if source == "native":

            executor = tool.get(
                "executor"
            )

            if not executor:

                return {
                    "success": False,
                    "tool": tool_name,
                    "error": (
                        "Native tool executor "
                        "is not configured."
                    )
                }

            try:

                result = executor(
                    **arguments
                )

                return {
                    "success": True,
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result
                }

            except Exception as error:

                return {
                    "success": False,
                    "tool": tool_name,
                    "arguments": arguments,
                    "error": str(error)
                }

        # =================================================
        # UNKNOWN SOURCE
        # =================================================

        return {
            "success": False,
            "tool": tool_name,
            "error": (
                f"Unknown tool source: {source}"
            )
        }