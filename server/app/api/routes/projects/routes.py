from typing import Any, cast
from fastapi import APIRouter
from bson import ObjectId

from app.services.database.mongodb import types, collections
from app.api.routes import schemas
from app.api import exceptions

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.get('', response_model=schemas.Projects)
def get_projects() -> Any:
    projects = collections.projects.get_projects()
    return schemas.Projects(
        projects=[schemas.Project.from_doc(doc=project) for project in projects]
    )


@router.post('', response_model=schemas.Project)
def create_project(
    request: schemas.CreateOrUpdateProject
) -> Any:
    project_id = collections.projects.create_project(name=request.name)
    project = cast(types.Project, collections.projects.get_project(project_id=project_id))
    return schemas.Project.from_doc(doc=project)


@router.get('/{project_id}', response_model=schemas.Project)
def get_project(
    project_id: str
) -> Any:
    project = collections.projects.get_project(project_id=ObjectId(project_id))
    if not project:
        raise exceptions.NotFoundException

    return schemas.Project.from_doc(doc=project)


@router.put('/{project_id}', response_model=schemas.Project)
def update_project(
    project_id: str,
    request: schemas.CreateOrUpdateProject
) -> Any:
    matched = collections.projects.update_project(project_id=ObjectId(project_id), name=request.name)
    if not matched:
        raise exceptions.NotFoundException

    project = cast(types.Project, collections.projects.get_project(project_id=ObjectId(project_id)))
    return schemas.Project.from_doc(doc=project)


@router.delete('/{project_id}', response_model=schemas.SuccessResponse)
def delete_project(
    project_id: str
) -> Any:
    deleted = collections.projects.delete_project(project_id=ObjectId(project_id))
    if not deleted:
        raise exceptions.NotFoundException

    return schemas.SuccessResponse(success=True)
