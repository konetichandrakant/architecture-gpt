from app.schemas.auth import LoginRequest, LoginResponse, CreateAccountRequest, CreateAccountResponse


class AuthService:

    def __init__(self):
        pass

    # request : {email, password} and response : {token, message}
    # call db and verify whether the email is present and if present whether password is right or wrong if it is wrong return error throwing incorrect email or password
    # else return token, message
    def login(request: LoginRequest):
        return LoginResponse()

    # request : {email, name, password} and response : {token, message}
    # call db and verify whether the email is present if present return email already exists
    # else return token, message
    def create_account(request: CreateAccountRequest):
        return CreateAccountResponse()

    # verify the token with jwt secret key and verify the output matches the format which is {user_id:str}
    def validate_token_and_extract_user_id(token: str):
        pass
