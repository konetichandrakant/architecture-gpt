from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.projects import Project
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


class ProjectService:

    def __init__(self) -> None:
        pass

    @classmethod
    def _get_or_404(cls, db: Session, id: str | int) -> Project:
        try:
            project = db.get(Project, int(id))
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="invalid project id")
        if project is None:
            raise HTTPException(status_code=404, detail="project not found")
        return project

    @classmethod
    def create(cls, request: CreateProjectRequest, db: Session) -> CreateProjectResponse:
        project = Project(title=request.title, description=request.description)
        db.add(project)
        db.commit()
        db.refresh(project)
        return CreateProjectResponse(id=str(project.id))

    @classmethod
    def list(cls, limit: int, db: Session) -> list[GetProjectResponse]:
        projects = db.query(Project).order_by(Project.id.desc()).limit(limit).all()
        return [
            GetProjectResponse(
                id=project.id,
                title=project.title,
                description=project.description,
                architecture_image_url=f"/api/v1/architectures/{project.architecture_id}" if project.architecture_id else "",
            )
            for project in projects
        ]

    @classmethod
    def get(cls, request: GetProjectDetailsRequest, db: Session) -> GetProjectDetailsResponse:
        project = cls._get_or_404(db, request.id)
        return GetProjectDetailsResponse(
            title=project.title,
            description=project.description,
            architecture_id=str(project.architecture_id) if project.architecture_id else "",
        )

    @classmethod
    def update(cls, id: int, request: UpdateProjectDetailsRequest, db: Session) -> UpdateProjectDetailsResponse:
        project = cls._get_or_404(db, id)
        project.title = request.title
        project.description = request.description
        if request.architecture_id:
            project.architecture_id = int(request.architecture_id)
        db.commit()
        return UpdateProjectDetailsResponse(message="project updated")

    @classmethod
    def delete(cls, request: ProjectDeleteRequest, db: Session) -> ProjectDeleteResponse:
        project = cls._get_or_404(db, request.id)
        db.delete(project)
        db.commit()
        return ProjectDeleteResponse(message="project deleted")
