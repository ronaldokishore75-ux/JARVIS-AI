# =========================================================
# JARVIS V7.8 - UNIFIED TOOL SELECTOR
# =========================================================

import json
import re

from local_llm import ask_local_raw


class UnifiedToolSelector:

    def __init__(self, registry):
        self.registry = registry

    # =====================================================
    # BUILD MODEL TOOL DEFINITIONS
    # =====================================================

    def _build_tool_prompt(self):

        tools = self.registry.get_all_tools()

        definitions = []

        for tool in tools:

            definitions.append(
                {
                    "name": tool["name"],
                    "description": tool.get(
                        "description",
                        ""
                    ),
                    "parameters": tool.get(
                        "parameters",
                        {
                            "type": "object",
                            "properties": {}
                        }
                    ),
                }
            )

        return json.dumps(
            definitions,
            indent=2,
            ensure_ascii=False
        )

    # =====================================================
    # DETECT CLEAR NO-TOOL REQUESTS
    # =====================================================

    def _looks_like_no_tool_request(
        self,
        command
    ):

        text = command.strip().lower()

        if not text:
            return True

        no_tool_patterns = [
            r"^what\s+is\b",
            r"^what\s+are\b",
            r"^who\s+is\b",
            r"^who\s+are\b",
            r"^why\s+is\b",
            r"^why\s+are\b",
            r"^how\s+does\b",
            r"^how\s+do\b",
            r"^how\s+can\b",
            r"^tell\s+me\s+about\b",
            r"^tell\s+me\s+a\s+fact\b",
            r"^tell\s+me\s+a\s+short\s+fact\b",
            r"^explain\b",
            r"^describe\b",
            r"^say\s+hello\b",
            r"^introduce\s+yourself\b",
            r"^who\s+are\s+you\b",
        ]

        for pattern in no_tool_patterns:

            if re.search(
                pattern,
                text
            ):

                return True

        return False

    # =====================================================
    # PARSE JSON
    # =====================================================

    def _parse_selection(
        self,
        text
    ):

        if not text:
            return None

        text = text.strip()

        # Remove markdown fences
        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()

        # Repair common Qwen typo
        text = text.replace(
            '"arguments{}',
            '"arguments":{}'
        )

        text = text.replace(
            "'arguments{}",
            '"arguments":{}'
        )

        start = text.find("{")
        end = text.rfind("}")

        if (
            start == -1
            or end == -1
            or end <= start
        ):

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

    # =====================================================
    # SELECT TOOL
    # =====================================================

    def select(
        self,
        command
    ):

        if not command or not command.strip():

            return {
                "tool": None,
                "arguments": {}
            }

        # -------------------------------------------------
        # Deterministic no-tool guard
        # -------------------------------------------------

        if self._looks_like_no_tool_request(
            command
        ):

            print(
                "\nV7.8 ROUTER: No tool required."
            )

            return {
                "tool": None,
                "arguments": {}
            }

        # -------------------------------------------------
        # Build tool definitions
        # -------------------------------------------------

        tool_definitions = (
            self._build_tool_prompt()
        )

        prompt = f"""
You are JARVIS's tool router.

Available tools:
{tool_definitions}

User command:
{command}

Decide whether a tool is actually required.

Return ONLY JSON.

If a tool is required:
{{"tool":"TOOL_NAME","arguments":{{}}}}

If no tool is required:
{{"tool":null,"arguments":{{}}}}

Rules:
- Use only an exact tool name from the list.
- Use arguments that match the tool schema.
- General questions do NOT require tools.
- Requests for facts or explanations do NOT require tools.
- Do not search a website unless the user explicitly asks you to search it.
- Do not explain your decision.
- Do not output markdown.
- Output JSON only.
"""

        raw = ask_local_raw(
            prompt
        )

        print(
            "\nV7.8 RAW MODEL RESPONSE:"
        )

        print(
            raw
        )

        selection = self._parse_selection(
            raw
        )

        if not selection:

            return None

        tool_name = selection.get(
            "tool"
        )

        arguments = selection.get(
            "arguments",
            {}
        )

        # -------------------------------------------------
        # No tool selected
        # -------------------------------------------------

        if tool_name is None:

            return {
                "tool": None,
                "arguments": {}
            }

        # -------------------------------------------------
        # Validate arguments
        # -------------------------------------------------

        if not isinstance(
            arguments,
            dict
        ):

            return None

        # -------------------------------------------------
        # Validate tool exists
        # -------------------------------------------------

        tool = self.registry.get_tool(
            tool_name
        )

        if not tool:

            return None

        # -------------------------------------------------
        # Return normalized selection
        # -------------------------------------------------

        return {
            "tool": tool_name,
            "arguments": arguments,
            "source": tool.get(
                "source"
            )
        }