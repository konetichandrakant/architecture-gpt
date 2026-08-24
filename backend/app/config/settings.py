from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Architecture GPT API"
    debug: bool = True
    frontend_url: str = "http://localhost:5173"

    # database
    database_url: str = "sqlite:///./architecture_gpt.db"

    # auth
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # generation pipeline
    generation_quality_target: int = 80
    generation_max_iterations: int = 2

    # ignore LLM_* and provider keys that share the same .env file
    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
