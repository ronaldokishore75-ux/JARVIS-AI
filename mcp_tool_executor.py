# =========================================================
# JARVIS V7.5 - MCP TOOL EXECUTOR
# =========================================================

from mcp_client import MCPClient


class MCPToolExecutor:

    def __init__(self, server_script):

        self.server_script = server_script

        self.client = MCPClient(
            server_script
        )

    # =====================================================
    # EXECUTE MCP TOOL
    # =====================================================

    async def execute(
        self,
        tool_name,
        arguments=None
    ):

        print(
            f"V7.5 MCP TOOL CALL: {tool_name}"
        )

        print(
            f"V7.5 ARGUMENTS: {arguments or {}}"
        )

        result = await self.client.call_tool(
            tool_name,
            arguments or {}
        )

        # -------------------------------------------------
        # Error check
        # -------------------------------------------------

        if result.is_error:

            return {
                "success": False,
                "tool": tool_name,
                "arguments": arguments or {},
                "error": self._extract_result(
                    result
                ),
            }

        # -------------------------------------------------
        # Success
        # -------------------------------------------------

        value = self._extract_result(
            result
        )

        print(
            "V7.5 MCP TOOL RESULT:",
            value
        )

        return {
            "success": True,
            "tool": tool_name,
            "arguments": arguments or {},
            "result": value,
        }

    # =====================================================
    # EXTRACT MCP RESULT
    # =====================================================

    def _extract_result(
        self,
        result
    ):

        parts = []

        for content in result.content:

            if getattr(
                content,
                "type",
                None
            ) == "text":

                parts.append(
                    content.text
                )

            else:

                parts.append(
                    str(content)
                )

        if not parts:

            if result.structured_content:

                return result.structured_content

            return None

        return "\n".join(
            parts
        )