from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.projects import (
    CreateProjectRequest,
    CreateProjectResponse,
    GetProjectDetailsRequest,
    GetProjectDetailsResponse,
    GetProjectResponse,
    ProjectDeleteRequest,
    ProjectDeleteResponse,
    UpdateProjectDetailsRequest,
    UpdateProjectDetailsResponse,
)
from app.services.projects import ProjectService

router = APIRouter()


# create a new project
@router.post("", response_model=CreateProjectResponse)
def create_project(request: CreateProjectRequest, db: Session = Depends(get_db)):
    return ProjectService.create(request, db)


# list projects
@router.get("", response_model=list[GetProjectResponse])
def list_projects(limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)):
    return ProjectService.list(limit, db)


# get project details
@router.get("/{project_id}", response_model=GetProjectDetailsResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    return ProjectService.get(GetProjectDetailsRequest(id=project_id), db)


# update project details
@router.put("/{project_id}", response_model=UpdateProjectDetailsResponse)
def update_project(project_id: int, request: UpdateProjectDetailsRequest, db: Session = Depends(get_db)):
    return ProjectService.update(project_id, request, db)


# delete a project
@router.delete("/{project_id}", response_model=ProjectDeleteResponse)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    return ProjectService.delete(ProjectDeleteRequest(id=project_id), db)
