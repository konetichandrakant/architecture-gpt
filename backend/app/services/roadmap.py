from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.roadmap import Roadmap
from app.schemas.roadmap import GetRoadmapResponse, UpdateRoadmapRequest, UpdateRoadmapResponse


class RoadmapService:

    def __init__(self) -> None:
        pass

    @classmethod
    def get(cls, architecture_id: int, db: Session) -> GetRoadmapResponse:
        roadmap = db.query(Roadmap).filter(Roadmap.architecture_id == architecture_id).first()
        if roadmap is None:
            raise HTTPException(status_code=404, detail="roadmap not found for this architecture")
        return GetRoadmapResponse(architecture_id=architecture_id, data=roadmap.data)

    @classmethod
    def upsert(cls, architecture_id: int, data: dict[str, Any], db: Session) -> Roadmap:
        """Create or replace the roadmap attached to an architecture."""
        roadmap = db.query(Roadmap).filter(Roadmap.architecture_id == architecture_id).first()
        if roadmap is None:
            roadmap = Roadmap(architecture_id=architecture_id, data=data)
            db.add(roadmap)
        else:
            roadmap.data = data
        db.commit()
        db.refresh(roadmap)
        return roadmap

    @classmethod
    def update(cls, architecture_id: int, request: UpdateRoadmapRequest, db: Session) -> UpdateRoadmapResponse:
        cls.upsert(architecture_id, request.data, db)
        return UpdateRoadmapResponse(message="roadmap updated")
