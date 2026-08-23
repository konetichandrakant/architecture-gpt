from fastapi import APIRouter

from app.schemas.users import CreateUserRequest, CreateUserResponse, GetUserRequest, GetUserResponse
from app.services.users import UserService

router = APIRouter()

# create a new user
@router.post("/user", response_model=CreateUserResponse)
def create_user(request: CreateUserRequest):
    return UserService.create(request)

# get user information
@router.get("/user", response_model=GetUserResponse)
def get_user(request: GetUserRequest):
    return UserService.get(request)

# update - N/A

# delete - N/A
