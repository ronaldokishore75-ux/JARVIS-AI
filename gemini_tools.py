# =========================================================
# JARVIS V3.3 - GEMINI TOOL CALLING ADAPTER
# =========================================================

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import (
    get_tool_definitions,
    execute_tool,
)


# =========================================================
# LOAD .ENV
# =========================================================

env_path = os.path.join(
    os.path.dirname(__file__),
    ".env"
)

load_dotenv(env_path)

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:

    raise RuntimeError(
        "GEMINI_API_KEY was not found in .env"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=api_key
)


# =========================================================
# BUILD GEMINI TOOL
# =========================================================

def get_gemini_tools():

    function_declarations = []

    for tool in get_tool_definitions():

        declaration = types.FunctionDeclaration(
            name=tool["name"],
            description=tool["description"],
            parameters_json_schema=tool["parameters"],
        )

        function_declarations.append(
            declaration
        )

    return types.Tool(
        function_declarations=function_declarations
    )


# =========================================================
# ASK GEMINI WITH TOOLS
# =========================================================

def ask_gemini_with_tools(prompt):

    gemini_tool = get_gemini_tools()

    config = types.GenerateContentConfig(
        tools=[
            gemini_tool
        ],
        automatic_function_calling=(
            types.AutomaticFunctionCallingConfig(
                disable=True
            )
        ),
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=config,
    )

    return response, (
        response.function_calls or []
    )


# =========================================================
# EXECUTE GEMINI TOOL CALLS
# =========================================================

def execute_gemini_tool_calls(
    function_calls
):

    results = []

    for call in function_calls:

        tool_name = call.name

        arguments = dict(
            call.args or {}
        )

        print(
            f"V3 TOOL CALL: {tool_name}"
        )

        print(
            f"V3 ARGUMENTS: {arguments}"
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

        results.append(
            {
                "name": tool_name,
                "arguments": arguments,
                "result": result,
            }
        )

    return results


# =========================================================
# RUN COMPLETE GEMINI TOOL-CALL CYCLE
# =========================================================

def run_tool_call_cycle(prompt):

    # -----------------------------------------------------
    # Step 1: Build Gemini tool
    # -----------------------------------------------------

    gemini_tool = get_gemini_tools()

    config = types.GenerateContentConfig(
        tools=[
            gemini_tool
        ],
        automatic_function_calling=(
            types.AutomaticFunctionCallingConfig(
                disable=True
            )
        ),
    )

    # -----------------------------------------------------
    # Step 2: User message
    # -----------------------------------------------------

    user_content = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=prompt
            )
        ]
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            user_content
        ],
        config=config,
    )

    function_calls = (
        response.function_calls or []
    )

    # -----------------------------------------------------
    # No tool call
    # -----------------------------------------------------

    if not function_calls:

        return {
            "response": response.text or "",
            "tool_calls": [],
            "results": [],
        }

    # -----------------------------------------------------
    # Step 3: Execute tools
    # -----------------------------------------------------

    results = []

    for call in function_calls:

        tool_name = call.name

        arguments = dict(
            call.args or {}
        )

        print(
            f"V3 TOOL CALL: {tool_name}"
        )

        print(
            f"V3 ARGUMENTS: {arguments}"
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
            f"V3 TOOL RESULT: {result}"
        )

        results.append(
            {
                "name": tool_name,
                "arguments": arguments,
                "result": result,
  
              
            }
        )

    # -----------------------------------------------------
    # Step 4: Preserve Gemini's function-call message
    # -----------------------------------------------------

    function_call_content = (
        response.candidates[0].content
    )

    # -----------------------------------------------------
    # Step 5: Build function response parts
    # -----------------------------------------------------

    function_response_parts = []

    for item in results:

        part = types.Part.from_function_response(
            name=item["name"],
            response={
                "result": item["result"]
            },
         
        )

        function_response_parts.append(
            part
        )

    # IMPORTANT:
    # Gemini GenerateContent expects this function
    # response content with role="user".
    function_response_content = types.Content(
        role="user",
        parts=function_response_parts
    )

    # -----------------------------------------------------
    # Step 6: Send result back to Gemini
    # -----------------------------------------------------

    final_response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            user_content,
            function_call_content,
            function_response_content,
        ],
        config=config,
    )

    # -----------------------------------------------------
    # Step 7: Final result
    # -----------------------------------------------------

    return {
        "response": final_response.text or "",
        "tool_calls": [
            {
                "name": call.name,
                "arguments": dict(
                    call.args or {}
                ),
            }
            for call in function_calls
        ],
        "results": results,
    }