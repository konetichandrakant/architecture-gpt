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
    xml_diagram: str

# Update

class UpdateArchitectureRequest(BaseModel):
    id: str
    xml_diagram: str

class UpdateArchitectureResponse(BaseModel):
    message: str

# Delete

class DeleteArchitectureRequest(BaseModel):
    id: str

class DeleteArchitectureResponse(BaseModel):
    message: str