from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Architecture GPT API"
    debug: bool = True
    frontend_url: str = "http://localhost:5173"

    model_config = {"env_file": ".env"}


settings = Settings()
