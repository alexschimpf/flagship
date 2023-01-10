from typing import Any
from fastapi import APIRouter

from app.api.routes.projects import schemas
from app.api.schemas import SuccessResponse
from app.api.routes.projects import controllers

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.get('', response_model=schemas.Projects)
def get_projects() -> Any:
    return controllers.get_projects.process()


@router.post('', response_model=schemas.ProjectWithPrivateKey)
def create_project(
    request: schemas.CreateOrUpdateProject
) -> Any:

    return controllers.create_project.process(request=request)


@router.get('/{project_id}', response_model=schemas.Project)
def get_project(
    project_id: str
) -> Any:
    return controllers.get_project.process(project_id=project_id)


@router.put('/{project_id}', response_model=schemas.Project)
def update_project(
    project_id: str,
    request: schemas.CreateOrUpdateProject
) -> Any:
    return controllers.update_project.process(
        project_id=project_id, request=request)


@router.delete('/{project_id}', response_model=SuccessResponse)
def delete_project(
    project_id: str
) -> Any:
    return controllers.delete_project.process(project_id=project_id)
