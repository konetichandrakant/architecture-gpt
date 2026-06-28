from fastapi import APIRouter
from schemas.architecture import CreateArchitectureRequest, CreateArchitectureResponse, DeleteArchitectureRequest, DeleteArchitectureResponse, GetArchitectureRequest, GetArchitectureResponse, UpdateArchitectureRequest, UpdateArchitectureResponse
from services.architecture import ArchitectureService

router = APIRouter()

@router.post("/architecture", response_model=CreateArchitectureResponse)
def create_architecture(request: CreateArchitectureRequest):
    return ArchitectureService.create(request)

@router.get("/architecture", response_model=GetArchitectureResponse)
def get_architecture(request: GetArchitectureRequest):
    return ArchitectureService.get(request)

@router.put("/architecture", response_model=UpdateArchitectureResponse)
def update_architecture(request: UpdateArchitectureRequest):
    return ArchitectureService.update(request)

@router.delete("/architecture", response_model=DeleteArchitectureResponse)
def delete_architecture(request: DeleteArchitectureRequest):
    return ArchitectureService.delete(request)
