from typing import Any

from pydantic import BaseModel

# Read

class GetRoadmapResponse(BaseModel):
    architecture_id: int
    data: dict[str, Any]

# Update (roadmaps stay editable after generation)

class UpdateRoadmapRequest(BaseModel):
    data: dict[str, Any]

class UpdateRoadmapResponse(BaseModel):
    message: str
