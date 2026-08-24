from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.generation import (
    CreateGenerationRequest,
    CreateGenerationResponse,
    GetGenerationResponse,
)
from app.services.generations import GenerationService

router = APIRouter()


# kick off a full pipeline run (architecture -> critique loop -> roadmap -> costs)
@router.post("", response_model=CreateGenerationResponse, status_code=status.HTTP_201_CREATED)
def create_generation(
    request: CreateGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    response = GenerationService.create_run(request, db)
    background_tasks.add_task(GenerationService.execute_run, response.id)
    return response


# poll a run: status, per-step model routing and spend
@router.get("/{generation_id}", response_model=GetGenerationResponse)
def get_generation(generation_id: int, db: Session = Depends(get_db)):
    return GenerationService.get(generation_id, db)


# list runs, optionally filtered by project
@router.get("", response_model=list[GetGenerationResponse])
def list_generations(
    project_id: int | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return GenerationService.list(project_id, limit, db)
