# =========================================================
# JARVIS V7.10 - MCP INTEGRATION BRIDGE
# =========================================================

import asyncio

from unified_tool_registry import UnifiedToolRegistry
from unified_tool_executor import UnifiedToolExecutor
from unified_tool_selector import UnifiedToolSelector


MCP_SERVER_SCRIPT = "mcp_test_server.py"


_registry = None
_selector = None
_executor = None


async def _get_mcp_components():

    global _registry
    global _selector
    global _executor

    if _registry is None:

        _registry = UnifiedToolRegistry(
            MCP_SERVER_SCRIPT
        )

        await _registry.discover_mcp_tools()

        _selector = UnifiedToolSelector(
            _registry
        )

        _executor = UnifiedToolExecutor(
            MCP_SERVER_SCRIPT
        )

    return (
        _registry,
        _selector,
        _executor
    )


async def _run_mcp_command(command):

    (
        registry,
        selector,
        executor
    ) = await _get_mcp_components()

    selection = selector.select(
        command
    )

    if not selection:
        return None

    if selection.get("tool") is None:
        return None

    tool = registry.get_tool(
        selection["tool"]
    )

    if not tool:
        return None

    result = await executor.execute(
        tool,
        selection.get(
            "arguments",
            {}
        )
    )

    if not result.get("success"):
        return None

    return (
        result.get("result")
        or f"Executed {result['tool']}."
    )


def try_mcp_tool_call(command):

    try:

        return asyncio.run(
            _run_mcp_command(
                command
            )
        )

    except Exception as error:

        print(

            f"V7.10 MCP ERROR:",

            repr(error)
        )

        return None