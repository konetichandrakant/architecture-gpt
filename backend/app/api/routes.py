from fastapi import APIRouter

from app.models.schemas import HealthResponse, MessageResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", message="API is running")


@router.get("/", response_model=MessageResponse)
async def root():
    return MessageResponse(message="Welcome to Architecture GPT API")
