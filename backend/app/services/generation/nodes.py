"""LangGraph node functions for the generation pipeline.

Each node calls exactly one routed use case through ModelRouter, records the
model/tokens/cost of the call into the state, and returns a partial state
update. Nodes whose artifact is non-critical degrade gracefully and log into
state["errors"] instead of killing the run.
"""

import re
from typing import Any

from app.config import settings
from app.services.generation import prompts
from app.services.generation.state import GenerationState
from app.services.llm.router import RouteResult, UseCase, get_model_router


def _record(state: GenerationState, step: str, result: RouteResult) -> dict[str, Any]:
    """Partial state update that appends one model call to the audit trail."""
    usage = list(state.get("model_usage", []))
    usage.append(
        {
            "step": step,
            "use_case": result.use_case,
            "model": result.model,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
            "cost_usd": result.cost_usd,
            "latency_seconds": result.latency_seconds,
        }
    )
    return {
        "model_usage": usage,
        "total_cost_usd": round(state.get("total_cost_usd", 0.0) + (result.cost_usd or 0.0), 6),
    }


def _extract_mxgraph(text: str) -> str:
    """Pull the mxGraphModel document out of a model reply."""
    match = re.search(r"<mxGraphModel.*</mxGraphModel>", text, re.DOTALL)
    if match:
        return match.group(0)
    fenced = re.search(r"```(?:xml)?\s*(.*?)```", text, re.DOTALL)
    return (fenced.group(1) if fenced else text).strip()


def analyze_requirements(state: GenerationState) -> dict[str, Any]:
    router = get_model_router()
    try:
        requirements, result = router.run_json(
            UseCase.ARCHITECTURE,
            prompts.build_analyze_messages(state["title"], state["description"]),
            temperature=0.1,
        )
    except Exception as exc:  # degraded analysis still lets the pipeline run
        requirements = {}
        result = None
        errors = list(state.get("errors", []))
        errors.append(f"requirement analysis failed: {exc}")
        return {"requirements": requirements, "errors": errors}

    if not requirements:
        requirements = {"product_summary": state["description"]}
    return {"requirements": requirements, **_record(state, "analyze", result)}


def _generate(state: GenerationState, improve: bool) -> dict[str, Any]:
    router = get_model_router()
    previous_xml = state.get("architecture_xml") if improve else None
    critique = state.get("critique") if improve else None

    result = router.run(
        UseCase.ARCHITECTURE,
        prompts.build_architecture_messages(state["requirements"], previous_xml, critique),
        temperature=0.3,
    )
    architecture_xml = _extract_mxgraph(result.content)
    if "<mxGraphModel" not in architecture_xml:
        raise ValueError("architecture model did not return a draw.io mxGraphModel document")

    update = _record(state, "improve" if improve else "architect", result)
    update["architecture_xml"] = architecture_xml
    update["iterations"] = state.get("iterations", 0) + 1
    return update


def generate_architecture(state: GenerationState) -> dict[str, Any]:
    return _generate(state, improve=False)


def improve_architecture(state: GenerationState) -> dict[str, Any]:
    return _generate(state, improve=True)


def critique_architecture(state: GenerationState) -> dict[str, Any]:
    router = get_model_router()
    try:
        critique, result = router.run_json(
            UseCase.CRITIQUE,
            prompts.build_critique_messages(state["requirements"], state["architecture_xml"]),
            temperature=0.1,
        )
    except Exception as exc:
        # no critique -> assume the target is met so the pipeline still finishes
        errors = list(state.get("errors", []))
        errors.append(f"critique failed, skipping improvement loop: {exc}")
        return {"critique": {}, "quality_score": settings.generation_quality_target, "errors": errors}

    try:
        score = int(critique.get("score", 0))
    except (TypeError, ValueError):
        score = 0
    return {"critique": critique, "quality_score": max(0, min(100, score)), **_record(state, "critic", result)}


def generate_roadmap(state: GenerationState) -> dict[str, Any]:
    router = get_model_router()
    try:
        roadmap, result = router.run_json(
            UseCase.ROADMAP,
            prompts.build_roadmap_messages(state["requirements"], state["architecture_xml"], state["critique"]),
            temperature=0.2,
        )
    except Exception as exc:
        roadmap = {}
        result = None
        errors = list(state.get("errors", []))
        errors.append(f"roadmap generation failed: {exc}")
        return {"roadmap": roadmap, "errors": errors}
    return {"roadmap": roadmap, **_record(state, "roadmap", result)}


def estimate_costs(state: GenerationState) -> dict[str, Any]:
    router = get_model_router()
    try:
        costs, result = router.run_json(
            UseCase.COSTS,
            prompts.build_costs_messages(state["requirements"], state["architecture_xml"], state["roadmap"]),
            temperature=0.1,
        )
    except Exception as exc:
        costs = {}
        result = None
        errors = list(state.get("errors", []))
        errors.append(f"cost estimation failed: {exc}")
        return {"costs": costs, "errors": errors}
    return {"costs": costs, **_record(state, "costs", result)}
