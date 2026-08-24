from fastapi import APIRouter

from app.api.v1.endpoints import architecture, auth, generations, projects, prompts, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(architecture.router, prefix="/architectures", tags=["architectures"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(generations.router, prefix="/generations", tags=["generations"])
