from pydantic import BaseModel

# Create

class CreateAccountRequest(BaseModel):
    name: str
    email: str
    password: str

class CreateAccountResponse(BaseModel):
    token: str
    message: str
    
# Read

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    message: str

# Update --> no use

# Delete --> no use