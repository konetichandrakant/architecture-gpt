from app.schemas.users import CreateUserRequest, CreateUserResponse, GetUserRequest, GetUserResponse


class UserService:

    def __init__(self) -> None:
        pass

    def create(self, request: CreateUserRequest) -> CreateUserResponse:
        pass

    def get(self, request: GetUserRequest) -> GetUserResponse:
        pass
