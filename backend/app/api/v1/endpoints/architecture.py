from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.architecture import (
    CreateArchitectureRequest,
    CreateArchitectureResponse,
    DeleteArchitectureRequest,
    DeleteArchitectureResponse,
    GetArchitectureRequest,
    GetArchitectureResponse,
    UpdateArchitectureRequest,
    UpdateArchitectureResponse,
)
from app.schemas.roadmap import GetRoadmapResponse, UpdateRoadmapRequest, UpdateRoadmapResponse
from app.schemas.costs import GetCostsResponse, UpdateCostsRequest, UpdateCostsResponse
from app.services.architecture import ArchitectureService
from app.services.roadmap import RoadmapService
from app.services.costs import CostService

router = APIRouter()


@router.post("", response_model=CreateArchitectureResponse)
def create_architecture(request: CreateArchitectureRequest, db: Session = Depends(get_db)):
    return ArchitectureService.create(request, db)


@router.get("/{architecture_id}", response_model=GetArchitectureResponse)
def get_architecture(architecture_id: str, db: Session = Depends(get_db)):
    return ArchitectureService.get(GetArchitectureRequest(id=architecture_id), db)


@router.put("/{architecture_id}", response_model=UpdateArchitectureResponse)
def update_architecture(architecture_id: str, request: UpdateArchitectureRequest, db: Session = Depends(get_db)):
    return ArchitectureService.update(architecture_id, request, db)


@router.delete("/{architecture_id}", response_model=DeleteArchitectureResponse)
def delete_architecture(architecture_id: str, db: Session = Depends(get_db)):
    return ArchitectureService.delete(DeleteArchitectureRequest(id=architecture_id), db)


# roadmap sub-resource (editable)

@router.get("/{architecture_id}/roadmap", response_model=GetRoadmapResponse)
def get_roadmap(architecture_id: int, db: Session = Depends(get_db)):
    return RoadmapService.get(architecture_id, db)


@router.put("/{architecture_id}/roadmap", response_model=UpdateRoadmapResponse)
def update_roadmap(architecture_id: int, request: UpdateRoadmapRequest, db: Session = Depends(get_db)):
    return RoadmapService.update(architecture_id, request, db)


# infrastructure cost sub-resource (editable)

@router.get("/{architecture_id}/costs", response_model=GetCostsResponse)
def get_costs(architecture_id: int, db: Session = Depends(get_db)):
    return CostService.get(architecture_id, db)


@router.put("/{architecture_id}/costs", response_model=UpdateCostsResponse)
def update_costs(architecture_id: int, request: UpdateCostsRequest, db: Session = Depends(get_db)):
    return CostService.update(architecture_id, request, db)
