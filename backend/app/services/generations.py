"""Orchestrates pipeline runs: DB bookkeeping around the LangGraph pipeline."""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.architecture import Architecture
from app.models.generation import Generation
from app.models.projects import Project
from app.schemas.generation import (
    CreateGenerationRequest,
    CreateGenerationResponse,
    GetGenerationResponse,
    ModelUsageEntry,
)
from app.services.generation.graph import run_generation
from app.services.costs import CostService
from app.services.roadmap import RoadmapService

logger = logging.getLogger(__name__)


class GenerationService:

    def __init__(self) -> None:
        pass

    @classmethod
    def _get_or_404(cls, db: Session, generation_id: int) -> Generation:
        generation = db.get(Generation, generation_id)
        if generation is None:
            raise HTTPException(status_code=404, detail="generation not found")
        return generation

    @classmethod
    def create_run(cls, request: CreateGenerationRequest, db: Session) -> CreateGenerationResponse:
        project = db.get(Project, request.project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="project not found")
        generation = Generation(project_id=request.project_id, status="queued")
        db.add(generation)
        db.commit()
        db.refresh(generation)
        return CreateGenerationResponse(
            id=generation.id,
            project_id=generation.project_id,
            status=generation.status,
            message="generation queued",
        )

    @classmethod
    def execute_run(cls, generation_id: int) -> None:
        """Run the pipeline and persist artifacts.

        Runs inside a FastAPI BackgroundTask with its own session; every
        failure mode ends in status='failed' with the error recorded.
        """
        with SessionLocal() as db:
            generation = db.get(Generation, generation_id)
            if generation is None:
                logger.error("generation %s vanished before execution", generation_id)
                return

            project = db.get(Project, generation.project_id)
            generation.status = "running"
            db.commit()

            try:
                final_state = run_generation(project.title, project.description)

                architecture = Architecture(
                    xml_diagram=final_state["architecture_xml"],
                    quality_score=final_state.get("quality_score"),
                    model_used=_final_architecture_model(final_state.get("model_usage", [])),
                    iterations=final_state.get("iterations", 0),
                )
                db.add(architecture)
                db.flush()

                RoadmapService.upsert(architecture.id, final_state.get("roadmap", {}), db)
                CostService.upsert(architecture.id, final_state.get("costs", {}), db)

                project.architecture_id = architecture.id
                generation.architecture_id = architecture.id
                generation.model_usage = final_state.get("model_usage", [])
                generation.total_cost_usd = final_state.get("total_cost_usd", 0.0)
                generation.status = "completed"
            except Exception as exc:
                logger.exception("generation %s failed", generation_id)
                generation.status = "failed"
                generation.error = str(exc)
            finally:
                db.commit()

    @classmethod
    def get(cls, generation_id: int, db: Session) -> GetGenerationResponse:
        generation = cls._get_or_404(db, generation_id)
        architecture = db.get(Architecture, generation.architecture_id) if generation.architecture_id else None
        return GetGenerationResponse(
            id=generation.id,
            project_id=generation.project_id,
            architecture_id=generation.architecture_id,
            status=generation.status,
            error=generation.error,
            quality_score=architecture.quality_score if architecture else None,
            iterations=architecture.iterations if architecture else 0,
            model_usage=[ModelUsageEntry(**entry) for entry in generation.model_usage],
            total_cost_usd=generation.total_cost_usd,
            created_at=generation.created_at,
            updated_at=generation.updated_at,
        )

    @classmethod
    def list(cls, project_id: int | None, limit: int, db: Session) -> list[GetGenerationResponse]:
        query = db.query(Generation)
        if project_id is not None:
            query = query.filter(Generation.project_id == project_id)
        generations = query.order_by(Generation.id.desc()).limit(limit).all()
        return [cls.get(generation.id, db) for generation in generations]


def _final_architecture_model(model_usage: list[dict]) -> str | None:
    """The model that produced the final diagram (last architecture call)."""
    models = [entry.get("model", "") for entry in model_usage if entry.get("use_case") == "architecture"]
    return models[-1] if models else None
