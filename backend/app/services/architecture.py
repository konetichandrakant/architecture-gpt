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


class ArchitectureService:

    def __init__(self):
        pass

    def create(self, request: CreateArchitectureRequest) -> CreateArchitectureResponse:
        pass

    def get(self, request: GetArchitectureRequest) -> GetArchitectureResponse:
        pass

    def update(self, request: UpdateArchitectureRequest) -> UpdateArchitectureResponse:
        pass

    def delete(self, request: DeleteArchitectureRequest) -> DeleteArchitectureResponse:
        pass
