import json
import re
import time
from enum import Enum
from typing import Any

import litellm
from litellm import Router
from pydantic import BaseModel

from app.config.llm import llm_settings


class UseCase(str, Enum):
    """Every pipeline step that needs an LLM routes through one of these groups."""

    ARCHITECTURE = "architecture"
    CRITIQUE = "critique"
    ROADMAP = "roadmap"
    COSTS = "costs"
    EDIT = "edit"


USE_CASE_SETTINGS = {
    UseCase.ARCHITECTURE: "architecture_models",
    UseCase.CRITIQUE: "critique_models",
    UseCase.ROADMAP: "roadmap_models",
    UseCase.COSTS: "costs_models",
    UseCase.EDIT: "edit_models",
}


class RouteResult(BaseModel):
    """Outcome of one routed completion call."""

    use_case: str
    model: str
    content: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float | None = None
    latency_seconds: float = 0.0


def extract_json(text: str) -> dict[str, Any]:
    """Parse the first JSON object out of a model reply.

    Models like wrapping JSON in markdown fences or adding prose around it,
    so pull the outermost ``{...}`` block and parse that.
    """
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text
    start, end = candidate.find("{"), candidate.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("model response contained no json object")
    return json.loads(candidate[start : end + 1])


class ModelRouter:
    """Routes each use case to its own fleet of SOTA models via litellm.

    Every use case maps to a litellm Router model group holding deployments
    from different providers. litellm retries a failing deployment by
    failing over to the next provider in the group, so one dead API key
    never kills a pipeline run.
    """

    def __init__(self):
        self._router = Router(
            model_list=self._build_model_list(),
            routing_strategy="usage-based-routing",
            num_retries=llm_settings.num_retries,
            timeout=llm_settings.request_timeout,
            cooldown_time=llm_settings.cooldown_time,
        )

    @staticmethod
    def _models_for(use_case: UseCase) -> list[str]:
        raw = getattr(llm_settings, USE_CASE_SETTINGS[use_case])
        models = [model.strip() for model in raw.split(",") if model.strip()]
        if not models:
            raise ValueError(f"no models configured for use case '{use_case.value}'")
        return models

    @classmethod
    def _build_model_list(cls) -> list[dict[str, Any]]:
        deployments: list[dict[str, Any]] = []
        for use_case in UseCase:
            for model in cls._models_for(use_case):
                deployments.append(
                    {
                        "model_name": use_case.value,
                        "litellm_params": {"model": model},
                    }
                )
        if not deployments:
            raise ValueError("no LLM deployments configured")
        return deployments

    def run(
        self,
        use_case: UseCase,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 8192,
    ) -> RouteResult:
        started = time.perf_counter()
        response = self._router.completion(
            model=use_case.value,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        latency = time.perf_counter() - started

        usage = getattr(response, "usage", None)
        input_tokens = getattr(usage, "prompt_tokens", 0) or 0
        output_tokens = getattr(usage, "completion_tokens", 0) or 0

        try:
            cost_usd = litellm.completion_cost(completion_response=response)
        except Exception:
            # unknown model pricing should never fail a pipeline run
            cost_usd = None

        return RouteResult(
            use_case=use_case.value,
            model=getattr(response, "model", "") or "",
            content=response.choices[0].message.content or "",
            input_tokens=int(input_tokens),
            output_tokens=int(output_tokens),
            cost_usd=cost_usd,
            latency_seconds=round(latency, 3),
        )

    def run_json(
        self,
        use_case: UseCase,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 8192,
    ) -> tuple[dict[str, Any], RouteResult]:
        """Run a completion and parse the reply as JSON."""
        result = self.run(use_case, messages, temperature=temperature, max_tokens=max_tokens)
        return extract_json(result.content), result


_model_router: ModelRouter | None = None


def get_model_router() -> ModelRouter:
    """Process-wide singleton, built lazily so importing the app stays cheap."""
    global _model_router
    if _model_router is None:
        _model_router = ModelRouter()
    return _model_router
