from fastapi import APIRouter

from app.schemas.architecture import (
    CreateArchitectureRequest,
    CreateArchitectureResponse,
    DeleteArchitectureRequest,
    DeleteArchitectureResponse,
    GetArchitectureRequest,
    GetArchitectureResponse,
    UpdateArchitectureRequest,
    UpdateArchitectureResponse,
)
from app.services.architecture import ArchitectureService

router = APIRouter()

# implemented in the CRUD commit along with roadmap/cost sub-resources
