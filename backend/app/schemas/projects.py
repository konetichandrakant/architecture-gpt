from pydantic import BaseModel

# Create

class CreateProjectRequest(BaseModel):
    title: str
    description: str

class CreateProjectResponse(BaseModel):
    id: str

# Read

class GetProjectRequest(BaseModel):
    limit: int

class GetProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    architecture_image_url: str

class GetProjectDetailsRequest(BaseModel):
    id: str

class GetProjectDetailsResponse(BaseModel):
    title: str
    description: str
    architecture_id: str

# Update

class UpdateProjectDetailsRequest(BaseModel):
    id: int
    title: str
    description: str
    architecture_id: str

class UpdateProjectDetailsResponse(BaseModel):
    message: str

# Delete

class ProjectDeleteRequest(BaseModel):
    id: int

class ProjectDeleteResponse(BaseModel):
    message: str