from typing import Any, TypedDict


class GenerationState(TypedDict):
    """State threaded through the generation graph.

    Nodes return partial dicts; LangGraph merges them into this state, so
    every key is the total value (lists are replaced, not appended).
    """

    # inputs
    title: str
    description: str

    # requirement analysis output (schema defined by the analyze prompt)
    requirements: dict[str, Any]

    # artifacts
    architecture_xml: str
    critique: dict[str, Any]
    roadmap: dict[str, Any]
    costs: dict[str, Any]

    # quality loop control
    quality_score: int
    iterations: int

    # bookkeeping
    model_usage: list[dict[str, Any]]
    total_cost_usd: float
    errors: list[str]
