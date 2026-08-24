from datetime import datetime

from pydantic import BaseModel

# Create (kicks off a pipeline run in the background)

class CreateGenerationRequest(BaseModel):
    project_id: int

class CreateGenerationResponse(BaseModel):
    id: int
    project_id: int
    status: str
    message: str

# Read

class ModelUsageEntry(BaseModel):
    step: str
    use_case: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float | None
    latency_seconds: float

class GetGenerationResponse(BaseModel):
    id: int
    project_id: int
    architecture_id: int | None
    status: str
    error: str | None
    quality_score: int | None
    iterations: int
    model_usage: list[ModelUsageEntry]
    total_cost_usd: float
    created_at: datetime
    updated_at: datetime
