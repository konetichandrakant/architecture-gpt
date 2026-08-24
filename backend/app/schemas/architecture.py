from pydantic import BaseModel

# Create

class CreateArchitectureRequest(BaseModel):
    xml_diagram: str

class CreateArchitectureResponse(BaseModel):
    id: str
    message: str

# Read

class GetArchitectureRequest(BaseModel):
    id: str

class GetArchitectureResponse(BaseModel):
    id: int
    xml_diagram: str
    quality_score: int | None = None
    model_used: str | None = None
    iterations: int = 0

# Update

class UpdateArchitectureRequest(BaseModel):
    xml_diagram: str

class UpdateArchitectureResponse(BaseModel):
    message: str

# Delete

class DeleteArchitectureRequest(BaseModel):
    id: str

class DeleteArchitectureResponse(BaseModel):
    message: str
