from pydantic import BaseModel

# Create

class CreateArchitectureRequest(BaseModel):
    architecture_diagram_xml: str

class CreateArchitectureResponse(BaseModel):
    id: str
    message: str
    
# Read

class GetArchitectureRequest(BaseModel):
    id: str

class GetArchitectureResponse(BaseModel):
    architecture_diagram_xml: str

# Update

class UpdateArchitectureRequest(BaseModel):
    id: str
    architecture_diagram_xml: str

class UpdateArchitectureResponse(BaseModel):
    message: str

# Delete

class DeleteArchitectureRequest(BaseModel):
    id: str

class DeleteArchitectureResponse(BaseModel):
    message: str