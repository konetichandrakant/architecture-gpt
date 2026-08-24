"""Prompt library for the generation pipeline.

Each builder returns a litellm/openai style message list and pairs with one
routed use case from app.services.llm.router.UseCase, so every step can run
on the model fleet best suited to it.
"""

import json
from typing import Any

ANALYZE_SYSTEM = """You are a senior software consultant. Turn a raw product idea into a crisp,
structured requirement analysis that an architect can design against.

Respond with ONLY a JSON object (no markdown, no prose) shaped like:
{
  "product_summary": "one paragraph restating what is being built",
  "functional_requirements": ["..."],
  "non_functional_requirements": ["performance, security, compliance, reliability ..."],
  "constraints": ["budget, team, deadlines, legacy systems ..."],
  "scale_assumptions": {"monthly_users": 0, "peak_rps": 0, "data_volume_gb": 0, "requests_per_user_per_day": 0},
  "suggested_stack": ["technology and why in one line"],
  "risks": ["..."]
}"""

ARCHITECTURE_SYSTEM = """You are a principal software architect producing editable diagrams.

Respond with ONLY a valid draw.io <mxGraphModel> XML document and nothing else:
no markdown fences, no commentary, no xml declaration. The XML must follow mxGraph
rules so it can be opened and edited directly in diagrams.net:

- one <root> containing <mxCell id="0"/> and <mxCell id="1" parent="0"/>
- every component is an <mxCell> with vertex="1", a unique id, value set to
  "Component name\n(technology)", and geometry with sane grid coordinates
- layer the diagram left to right: clients, edge/API gateway, services,
  data stores, external integrations, infrastructure
- every connection is an <mxCell> with edge="1", source and target set to
  component ids, and value set to the protocol/purpose ("HTTPS/REST", "gRPC",
  "pub/sub", "async")
- prefer managed cloud services over self-hosted equivalents
- include databases, caches, queues, load balancers, CDN, observability and
  auth where the requirements demand them
- the diagram must fully implement the requirements: no component mentioned
  by another component may be missing"""

CRITIQUE_SYSTEM = """You are a ruthless staff-level architecture reviewer. You receive a requirement
analysis and a draw.io architecture diagram and must judge whether the design
actually satisfies the requirements.

Respond with ONLY a JSON object (no markdown, no prose) shaped like:
{
  "score": 0,
  "summary": "two or three sentences on the overall quality",
  "issues": [
    {"severity": "critical|major|minor", "component": "which part of the diagram",
     "description": "what is wrong", "suggestion": "concrete fix"}
  ],
  "strengths": ["..."]
}

Score calibration (be strict):
- 0-49:  fundamentally broken, missing core components
- 50-69: plausible but has critical gaps (no cache, no auth, single point of failure)
- 70-79: solid design with major issues remaining
- 80-89: production-ready design, only minor issues
- 90-100: exemplary, nothing material to fix
Only award 80+ when a competent principal engineer would ship it."""

ROADMAP_SYSTEM = """You are a delivery lead turning an architecture into an implementation roadmap.

Respond with ONLY a JSON object (no markdown, no prose) shaped like:
{
  "summary": "one paragraph delivery strategy",
  "total_duration_weeks": 0,
  "phases": [
    {
      "name": "phase name",
      "goal": "what exists at the end of this phase",
      "duration_weeks": 0,
      "milestones": ["demoable checkpoint", "..."],
      "tasks": [
        {"title": "concrete task", "description": "how to do it", "dependencies": ["other task titles"]}
      ]
    }
  ]
}

Order phases by dependency (walking skeleton first, hardening and launch last),
keep each phase under 4 weeks, and make every task small enough for one engineer
to own."""

COSTS_SYSTEM = """You are a cloud cost estimator. Price the infrastructure in the architecture
diagram with realistic 2026 list prices for the scale given in the requirements.

Respond with ONLY a JSON object (no markdown, no prose) shaped like:
{
  "currency": "USD",
  "monthly_total_usd": 0.0,
  "items": [
    {"service": "Cloud SQL", "provider": "GCP", "spec": "db-custom-2-7680", "purpose": "primary postgres",
     "count": 1, "monthly_cost_usd": 0.0}
  ],
  "one_time_costs": [{"item": "migration engineering", "cost_usd": 0.0}],
  "assumptions": ["pricing assumptions made"],
  "cost_optimization_notes": ["cheaper alternatives worth considering"]
}

monthly_total_usd must equal the sum of all items. Prefer on-demand list prices
unless the requirements say committed use."""


def _dump(payload: Any) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


def build_analyze_messages(title: str, description: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": ANALYZE_SYSTEM},
        {
            "role": "user",
            "content": f"Product title: {title}\n\nProduct description:\n{description}",
        },
    ]


def build_architecture_messages(
    requirements: dict[str, Any],
    previous_xml: str | None = None,
    critique: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    parts = [f"Requirement analysis:\n{_dump(requirements)}"]
    if previous_xml and critique:
        parts.append(f"Current diagram (scored {critique.get('score', '?')}/100):\n{previous_xml}")
        parts.append(
            "Reviewer feedback to address — regenerate the full improved diagram:\n"
            + _dump(critique.get("issues", []))
        )
    return [
        {"role": "system", "content": ARCHITECTURE_SYSTEM},
        {"role": "user", "content": "\n\n".join(parts)},
    ]


def build_critique_messages(requirements: dict[str, Any], architecture_xml: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": CRITIQUE_SYSTEM},
        {
            "role": "user",
            "content": f"Requirement analysis:\n{_dump(requirements)}\n\nArchitecture diagram XML:\n{architecture_xml}",
        },
    ]


def build_roadmap_messages(
    requirements: dict[str, Any], architecture_xml: str, critique: dict[str, Any]
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": ROADMAP_SYSTEM},
        {
            "role": "user",
            "content": (
                f"Requirement analysis:\n{_dump(requirements)}\n\n"
                f"Architecture diagram XML:\n{architecture_xml}\n\n"
                f"Known weaknesses to sequence around:\n{_dump(critique.get('issues', []))}"
            ),
        },
    ]


def build_costs_messages(
    requirements: dict[str, Any], architecture_xml: str, roadmap: dict[str, Any]
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": COSTS_SYSTEM},
        {
            "role": "user",
            "content": (
                f"Requirement analysis (scale assumptions drive the pricing):\n{_dump(requirements)}\n\n"
                f"Architecture diagram XML:\n{architecture_xml}\n\n"
                f"Delivery roadmap summary:\n{_dump(roadmap.get('summary', ''))}"
            ),
        },
    ]


def build_edit_messages(prompt: str, architecture_xml: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                ARCHITECTURE_SYSTEM
                + "\n\nYou are editing an existing diagram. Apply the requested change while keeping "
                "every unaffected component exactly as it is. Respond with ONLY the complete updated "
                "<mxGraphModel> XML document."
            ),
        },
        {
            "role": "user",
            "content": f"Current diagram:\n{architecture_xml}\n\nRequested change:\n{prompt}",
        },
    ]
