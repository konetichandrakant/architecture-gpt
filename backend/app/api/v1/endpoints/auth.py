from fastapi import APIRouter

from app.schemas.auth import CreateAccountRequest, CreateAccountResponse, LoginRequest, LoginResponse
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    return AuthService.login(request)


@router.post("/create-account", response_model=CreateAccountResponse)
def create_account(request: CreateAccountRequest):
    return AuthService.create_account(request)
