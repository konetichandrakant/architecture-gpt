from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.architecture import Architecture
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


class ArchitectureService:

    def __init__(self):
        pass

    @classmethod
    def _get_or_404(cls, db: Session, id: str) -> Architecture:
        try:
            architecture = db.get(Architecture, int(id))
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="invalid architecture id")
        if architecture is None:
            raise HTTPException(status_code=404, detail="architecture not found")
        return architecture

    @classmethod
    def create(cls, request: CreateArchitectureRequest, db: Session) -> CreateArchitectureResponse:
        architecture = Architecture(xml_diagram=request.xml_diagram)
        db.add(architecture)
        db.commit()
        db.refresh(architecture)
        return CreateArchitectureResponse(id=str(architecture.id), message="architecture created")

    @classmethod
    def get(cls, request: GetArchitectureRequest, db: Session) -> GetArchitectureResponse:
        architecture = cls._get_or_404(db, request.id)
        return GetArchitectureResponse(
            id=architecture.id,
            xml_diagram=architecture.xml_diagram,
            quality_score=architecture.quality_score,
            model_used=architecture.model_used,
            iterations=architecture.iterations,
        )

    @classmethod
    def update(cls, id: str, request: UpdateArchitectureRequest, db: Session) -> UpdateArchitectureResponse:
        architecture = cls._get_or_404(db, id)
        architecture.xml_diagram = request.xml_diagram
        db.commit()
        return UpdateArchitectureResponse(message="architecture updated")

    @classmethod
    def delete(cls, request: DeleteArchitectureRequest, db: Session) -> DeleteArchitectureResponse:
        architecture = cls._get_or_404(db, request.id)
        db.delete(architecture)
        db.commit()
        return DeleteArchitectureResponse(message="architecture deleted")
