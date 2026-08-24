"""LangGraph wiring for the generation pipeline.

    START -> analyze -> architect -> critic -+-> roadmap -> costs -> END
                                            |
                                            +-> improve -> critic  (loop)

The critic loop is the quality gate: the diagram is regenerated against the
critique until the review score reaches generation_quality_target (default 80)
or generation_max_iterations is exhausted, which is what pushes the generated
architecture well past a single-shot draft.
"""

from typing import Any

from langgraph.graph import END, START, StateGraph

from app.config import settings
from app.services.generation.nodes import (
    analyze_requirements,
    critique_architecture,
    estimate_costs,
    generate_architecture,
    generate_roadmap,
    improve_architecture,
)
from app.services.generation.state import GenerationState


def route_after_critique(state: GenerationState) -> str:
    """Keep improving the diagram until it scores at or above the target."""
    target_reached = state.get("quality_score", 0) >= settings.generation_quality_target
    budget_left = state.get("iterations", 0) < settings.generation_max_iterations
    if not target_reached and budget_left:
        return "improve"
    return "roadmap"


def build_generation_graph():
    builder = StateGraph(GenerationState)

    builder.add_node("analyze", analyze_requirements)
    builder.add_node("architect", generate_architecture)
    builder.add_node("critic", critique_architecture)
    builder.add_node("improve", improve_architecture)
    builder.add_node("roadmap", generate_roadmap)
    builder.add_node("costs", estimate_costs)

    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "architect")
    builder.add_edge("architect", "critic")
    builder.add_conditional_edges(
        "critic",
        route_after_critique,
        {"improve": "improve", "roadmap": "roadmap"},
    )
    builder.add_edge("improve", "critic")
    builder.add_edge("roadmap", "costs")
    builder.add_edge("costs", END)

    return builder.compile()


generation_graph = build_generation_graph()


def run_generation(title: str, description: str) -> dict[str, Any]:
    """Run the full pipeline and return the final state."""
    initial_state: GenerationState = {
        "title": title,
        "description": description,
        "requirements": {},
        "architecture_xml": "",
        "critique": {},
        "roadmap": {},
        "costs": {},
        "quality_score": 0,
        "iterations": 0,
        "model_usage": [],
        "total_cost_usd": 0.0,
        "errors": [],
    }
    return dict(generation_graph.invoke(initial_state))
