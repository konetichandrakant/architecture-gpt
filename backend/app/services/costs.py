from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.infrastructure_cost import InfrastructureCost
from app.schemas.costs import GetCostsResponse, UpdateCostsRequest, UpdateCostsResponse


class CostService:

    def __init__(self) -> None:
        pass

    @classmethod
    def get(cls, architecture_id: int, db: Session) -> GetCostsResponse:
        costs = db.query(InfrastructureCost).filter(InfrastructureCost.architecture_id == architecture_id).first()
        if costs is None:
            raise HTTPException(status_code=404, detail="cost estimate not found for this architecture")
        return GetCostsResponse(architecture_id=architecture_id, data=costs.data)

    @classmethod
    def upsert(cls, architecture_id: int, data: dict[str, Any], db: Session) -> InfrastructureCost:
        """Create or replace the cost estimate attached to an architecture."""
        costs = db.query(InfrastructureCost).filter(InfrastructureCost.architecture_id == architecture_id).first()
        if costs is None:
            costs = InfrastructureCost(architecture_id=architecture_id, data=data)
            db.add(costs)
        else:
            costs.data = data
        db.commit()
        db.refresh(costs)
        return costs

    @classmethod
    def update(cls, architecture_id: int, request: UpdateCostsRequest, db: Session) -> UpdateCostsResponse:
        cls.upsert(architecture_id, request.data, db)
        return UpdateCostsResponse(message="costs updated")
