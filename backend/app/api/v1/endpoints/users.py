from fastapi import APIRouter
from schemas.users import CreateUserRequest, CreateUserResponse, GetUserRequest, GetUserResponse
from services.users import UserService

router = APIRouter()

# create a new user
@router.post("/user", response_model=CreateUserRequest)
def create_user(request: CreateUserRequest):
    return UserService.create(request)

# get user information
@router.get("/user", response_model=GetUserResponse)
def get_user(request: GetUserRequest):
    return UserService.get(request)
    
# update - N/A

# delete - N/A