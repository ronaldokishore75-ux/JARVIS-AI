# =========================================================
# JARVIS V6.6 - LOCAL LLM + TOOL CALLING
# =========================================================

import json

from local_llm import ask_local,ask_local_raw
from tools import execute_tool, get_tool_definitions


# =========================================================
# BUILD TOOL DESCRIPTIONS FOR LOCAL MODEL
# =========================================================

def get_local_tool_prompt():

    tools = get_tool_definitions()

    lines = []

    for tool in tools:

        lines.append(
            json.dumps(
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"],
                },
                ensure_ascii=False
            )
        )

    return "\n".join(lines)


# =========================================================
# PARSE TOOL REQUEST
# =========================================================

def parse_tool_request(text):

    if not text:
        return None

    text = text.strip()

    # -----------------------------------------------------
    # Remove markdown code fences
    # -----------------------------------------------------

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    text = text.strip()

    # -----------------------------------------------------
    # Find JSON object
    # -----------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    candidate = text[
        start:end + 1
    ]

    try:

        data = json.loads(
            candidate
        )

    except json.JSONDecodeError:

        return None

    if not isinstance(
        data,
        dict
    ):
        return None

    return data


# =========================================================
# ASK LOCAL MODEL TO SELECT A TOOL
# =========================================================

def select_local_tool(command):

    tool_descriptions = (
        get_local_tool_prompt()
    )

    prompt = f"""
You are a tool-selection engine.

Available tools:

{tool_descriptions}

User command:
{command}

Return ONLY one JSON object.

For a tool call:
{{
  "tool": "open_youtube",
  "arguments": {{}}
}}

For a YouTube search:
{{
  "tool": "search_youtube",
  "arguments": {{
    "query": "Python tutorials"
  }}
}}

If no tool is required:
{{
  "tool": null,
  "arguments": {{}}
}}

No explanation.
No markdown.
No reasoning.
No additional text.
"""

    response = ask_local_raw(
        prompt
    )

    print(
        "\nV6.6 RAW LOCAL RESPONSE:"

    )

    print(
        response

    )


    return parse_tool_request(
        response
    )


# =========================================================
# EXECUTE LOCAL TOOL CALL
# =========================================================

def execute_local_tool_call(
    command
):

    request = select_local_tool(
        command
    )

    if not request:

        return {
            "success": False,
            "error": (
                "Local model did not return "
                "valid tool JSON."
            ),
        }

    tool_name = request.get(
        "tool"
    )

    arguments = request.get(
        "arguments",
        {}
    )

    if not tool_name:

        return {
            "success": True,
            "tool": None,
            "arguments": {},
            "result": None,
        }

    if not isinstance(
        arguments,
        dict
    ):

        return {
            "success": False,
            "error": (
                "Tool arguments must be "
                "a JSON object."
            ),
        }

    print(
        f"V6.6 LOCAL TOOL CALL: {tool_name}"
    )

    print(
        f"V6.6 ARGUMENTS: {arguments}"
    )

    try:

        result = execute_tool(
            tool_name,
            arguments
        )

    except Exception as error:

        result = {
            "error": str(error)
        }

    print(
        "V6.6 TOOL RESULT:",
        result
    )

    return {
        "success": "error" not in result,
        "tool": tool_name,
        "arguments": arguments,
        "result": result,
    }


# =========================================================
# COMPLETE LOCAL TOOL CYCLE
# =========================================================

def run_local_tool_cycle(
    command
):

    tool_result = execute_local_tool_call(
        command
    )

    # -----------------------------------------------------
    # No tool selected
    # -----------------------------------------------------

    if tool_result.get("tool") is None:

        return {
            "tool": None,
            "arguments": {},
            "result": None,
            "response": (
                "No tool was required."
            ),
        }

    # -----------------------------------------------------
    # Ask local model for final response
    # -----------------------------------------------------

    final_prompt = f"""
You are JARVIS.

The user requested:

{command}

The tool that was executed:
{tool_result["tool"]}

Tool arguments:
{tool_result["arguments"]}

Tool result:
{tool_result["result"]}

Give the user a concise final response.

Do not mention internal reasoning.
Do not mention Qwen.
Do not output JSON.
"""

    response = ask_local(
        final_prompt
    
    )


    return {
        "tool": tool_result["tool"],
        "arguments": tool_result["arguments"],
        "result": tool_result["result"],
        "response": response,
    }