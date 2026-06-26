from pydantic import BaseModel

# Create

class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str

class CreateUserResponse(BaseModel):
    id: str
    message: str

# Read

class GetUserRequest(BaseModel):
    id: str

class GetUserResponse(BaseModel):
    email: str
    username: str
    
# Update - N/A

# Delete - N/A