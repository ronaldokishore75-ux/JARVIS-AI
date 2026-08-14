# =========================================================
# JARVIS V3 - TOOL REGISTRY
# =========================================================

from dataclasses import dataclass
from typing import Callable, Any



from action import (
    open_youtube,
    search_youtube,
    scroll_down,
    scroll_up,
    click_link_by_name,
    set_volume,

    # V3.9 additional tools
    open_google,
    search_google,
    scroll_down_little,
    scroll_up_little,
    open_vscode,
    open_file_explorer,
    open_powershell,
    open_downloads,
    open_jarvis_folder,
    open_jarvis_vscode,
    open_chatgpt,
    open_gemini,
    mute_volume,
    unmute_volume,
)


# =========================================================
# TOOL DEFINITION
# =========================================================

@dataclass
class Tool:

    name: str
    description: str
    function: Callable
    parameters: dict


# =========================================================
# TOOL REGISTRY
# =========================================================

TOOLS = {}


def register_tool(
    name: str,
    description: str,
    function: Callable,
    parameters: dict
):

    TOOLS[name] = Tool(
        name=name,
        description=description,
        function=function,
        parameters=parameters
    )


# =========================================================
# IMPORT EXISTING JARVIS ACTIONS
# =========================================================

from action import (
    open_youtube,
    search_youtube,
    scroll_down,
    scroll_up,
    click_link_by_name,
    set_volume,
)


# =========================================================
# REGISTER TOOLS
# =========================================================

register_tool(
    name="open_youtube",
    description="Open YouTube in the JARVIS browser.",
    function=open_youtube,
    parameters={}
)


register_tool(
    name="search_youtube",
    description="Search YouTube for a query.",
    function=search_youtube,
    parameters={
        "query": {
            "type": "string",
            "description": "The YouTube search query."
        }
    }
)


register_tool(
    name="scroll_down",
    description="Scroll the current page downward.",
    function=scroll_down,
    parameters={}
)


register_tool(
    name="scroll_up",
    description="Scroll the current page upward.",
    function=scroll_up,
    parameters={}
)


register_tool(
    name="click_link",
    description="Find and click a visible link by name.",
    function=click_link_by_name,
    parameters={
        "link_name": {
            "type": "string",
            "description": "The text or name of the link to click."
        }
    }
)


register_tool(
    name="set_volume",
    description="Set the computer volume.",
    function=set_volume,
    parameters={
        "percent": {
            "type": "integer",
            "description": "Volume level from 0 to 100."
        }
    }
)

# =========================================================
# V3.9 - ADDITIONAL TOOLS
# =========================================================

register_tool(
    name="open_google",
    description="Open Google in the JARVIS browser.",
    function=open_google,
    parameters={}
)


register_tool(
    name="search_google",
    description="Search Google for a query.",
    function=search_google,
    parameters={
        "query": {
            "type": "string",
            "description": "The Google search query."
        }
    }
)


register_tool(
    name="scroll_down_little",
    description="Scroll the current page down by a small amount.",
    function=scroll_down_little,
    parameters={}
)


register_tool(
    name="scroll_up_little",
    description="Scroll the current page up by a small amount.",
    function=scroll_up_little,
    parameters={}
)


register_tool(
    name="open_vscode",
    description="Open Visual Studio Code.",
    function=open_vscode,
    parameters={}
)


register_tool(
    name="open_file_explorer",
    description="Open Windows File Explorer.",
    function=open_file_explorer,
    parameters={}
)


register_tool(
    name="open_powershell",
    description="Open PowerShell.",
    function=open_powershell,
    parameters={}
)


register_tool(
    name="open_downloads",
    description="Open the Downloads folder.",
    function=open_downloads,
    parameters={}
)


register_tool(
    name="open_jarvis_folder",
    description="Open the JARVIS project folder.",
    function=open_jarvis_folder,
    parameters={}
)


register_tool(
    name="open_jarvis_vscode",
    description="Open the JARVIS project in Visual Studio Code.",
    function=open_jarvis_vscode,
    parameters={}
)


register_tool(
    name="open_chatgpt",
    description="Open ChatGPT.",
    function=open_chatgpt,
    parameters={}
)


register_tool(
    name="open_gemini",
    description="Open Gemini.",
    function=open_gemini,
    parameters={}
)


register_tool(
    name="mute_volume",
    description="Mute the computer volume.",
    function=mute_volume,
    parameters={}
)


register_tool(
    name="unmute_volume",
    description="Unmute the computer volume.",
    function=unmute_volume,
    parameters={}
)


# =========================================================
# EXECUTE TOOL SAFELY
# =========================================================

def execute_tool(
    tool_name: str,
    arguments: dict | None = None
) -> Any:

    arguments = arguments or {}

    # -----------------------------------------------------
    # Tool lookup
    # -----------------------------------------------------

    tool = TOOLS.get(
        tool_name
    )

    if tool is None:

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    # -----------------------------------------------------
    # Validate arguments
    # -----------------------------------------------------

    validate_tool_arguments(
        tool,
        arguments
    )

    # -----------------------------------------------------
    # Execute
    # -----------------------------------------------------

    result = tool.function(
        **arguments
    )

    # -----------------------------------------------------
    # Normalize empty results
    # -----------------------------------------------------

    if result is None:

        return {
            "success": True,
            "message": (
                f"Tool '{tool_name}' "
                "executed successfully."
            )
        }

    return result


# =========================================================
# VALIDATE TOOL ARGUMENTS
# =========================================================

def validate_tool_arguments(
    tool: Tool,
    arguments: dict
):

    if arguments is None:

        arguments = {}

    # -----------------------------------------------------
    # Check required parameters
    # -----------------------------------------------------

    for parameter_name in tool.parameters:

        if parameter_name not in arguments:

            raise ValueError(
                f"Missing required argument: "
                f"{parameter_name}"
            )

    # -----------------------------------------------------
    # Validate known parameter types / ranges
    # -----------------------------------------------------

    for parameter_name, parameter_info in tool.parameters.items():

        value = arguments.get(
            parameter_name
        )

        expected_type = parameter_info.get(
            "type",
            "string"
        )

        if expected_type == "string":

            if not isinstance(
                value,
                str
            ):

                raise ValueError(
                    f"{parameter_name} "
                    "must be a string."
                )

        elif expected_type == "integer":

            if not isinstance(
                value,
                int
            ) or isinstance(
                value,
                bool
            ):

                raise ValueError(
                    f"{parameter_name} "
                    "must be an integer."
                )

    # -----------------------------------------------------
    # Volume safety
    # -----------------------------------------------------

    if tool.name == "set_volume":

        percent = arguments.get(
            "percent"
        )

        if percent < 0 or percent > 100:

            raise ValueError(
                "Volume level must be "
                "between 0 and 100."
            )

    return True


# =========================================================
# GET LLM-READY TOOL DEFINITIONS
# =========================================================

def get_tool_definitions():

    definitions = []

    for tool in TOOLS.values():

        properties = {}
        required = []

        for (
            parameter_name,
            parameter_info
        ) in tool.parameters.items():

            properties[parameter_name] = {
                "type": parameter_info.get(
                    "type",
                    "string"
                ),
                "description": parameter_info.get(
                    "description",
                    ""
                )
            }

            required.append(
                parameter_name
            )

        schema = {
            "type": "object",
            "properties": properties,
            "required": required,
        }

        definitions.append(
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": schema,
            }
        )

    return definitions