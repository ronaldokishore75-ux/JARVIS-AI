# =========================================================
# JARVIS V8.7.1 - EVALUATION FRAMEWORK
# =========================================================

from dataclasses import dataclass, field


@dataclass
class EvaluationCase:
    name: str
    command: str

    expected_route: str | None = None
    expected_response: str | None = None

    required_debug: list[str] = field(
        default_factory=list
    )

    forbidden_debug: list[str] = field(
        default_factory=list
    )


@dataclass
class EvaluationResult:
    name: str
    passed: bool

    route_ok: bool
    response_ok: bool
    required_debug_ok: bool
    forbidden_debug_ok: bool

    response: str | None
    debug_output: str

    errors: list[str] = field(
        default_factory=list
    )