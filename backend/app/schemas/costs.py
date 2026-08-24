from typing import Any

from pydantic import BaseModel

# Read

class GetCostsResponse(BaseModel):
    architecture_id: int
    data: dict[str, Any]

# Update (cost estimates stay editable after generation)

class UpdateCostsRequest(BaseModel):
    data: dict[str, Any]

class UpdateCostsResponse(BaseModel):
    message: str
