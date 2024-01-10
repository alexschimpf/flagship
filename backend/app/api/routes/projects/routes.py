from fastapi import APIRouter, Depends

from app.api import auth
from app.api.routes.projects.controllers.create_project import CreateProjectController
from app.api.routes.projects.controllers.create_project_private_key import CreateProjectPrivateKeyController
from app.api.routes.projects.controllers.delete_project import DeleteProjectController
from app.api.routes.projects.controllers.delete_project_private_key import DeleteProjectPrivateKeyController
from app.api.routes.projects.controllers.get_project import GetProjectController
from app.api.routes.projects.controllers.get_project_private_keys import GetProjectPrivateKeysController
from app.api.routes.projects.controllers.get_projects import GetProjectsController
from app.api.routes.projects.controllers.update_project import UpdateProjectController
from app.api.routes.projects.controllers.update_project_private_key import UpdateProjectPrivateKeyController
from app.api.routes.projects.schemas import Project, Projects, CreateOrUpdateProject, ProjectWithPrivateKey, \
    ProjectPrivateKey, ProjectPrivateKeyName, ProjectPrivateKeys
from app.api.schemas import SuccessResponse, User

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.get('', response_model=Projects)
def get_projects(me: User = Depends(auth.get_user)) -> Projects:
    return GetProjectsController(me=me).handle_request()


@router.post('', response_model=ProjectWithPrivateKey)
def create_project(
    request: CreateOrUpdateProject,
    me: User = Depends(auth.get_user)
) -> ProjectWithPrivateKey:
    return CreateProjectController(
        request=request,
        me=me
    ).handle_request()


@router.get('/{project_id}', response_model=Project)
def get_project(project_id: int, me: User = Depends(auth.get_user)) -> Project:
    return GetProjectController(
        project_id=project_id,
        me=me
    ).handle_request()


@router.put('/{project_id}', response_model=Project)
def update_project(
    project_id: int,
    request: CreateOrUpdateProject,
    me: User = Depends(auth.get_user)
) -> Project:
    return UpdateProjectController(
        project_id=project_id,
        request=request,
        me=me
    ).handle_request()


@router.delete('/{project_id}', response_model=SuccessResponse)
def delete_project(project_id: int, me: User = Depends(auth.get_user)) -> SuccessResponse:
    return DeleteProjectController(
        project_id=project_id,
        me=me
    ).handle_request()


@router.post('/{project_id}/private_keys', response_model=ProjectPrivateKey)
def create_project_private_key(
    project_id: int,
    request: ProjectPrivateKeyName,
    me: User = Depends(auth.get_user)
) -> ProjectPrivateKey:
    return CreateProjectPrivateKeyController(
        project_id=project_id,
        request=request,
        me=me
    ).handle_request()


@router.get('/{project_id}/private_keys', response_model=ProjectPrivateKeys)
def get_project_private_keys(
    project_id: int,
    me: User = Depends(auth.get_user)
) -> ProjectPrivateKeys:
    return GetProjectPrivateKeysController(
        project_id=project_id,
        me=me
    ).handle_request()


@router.put('/{project_id}/private_keys/{project_private_key_id}', response_model=SuccessResponse)
def update_project_private_key(
    project_id: int,
    project_private_key_id: int,
    request: ProjectPrivateKeyName,
    me: User = Depends(auth.get_user)
) -> SuccessResponse:
    return UpdateProjectPrivateKeyController(
        project_id=project_id,
        project_private_key_id=project_private_key_id,
        request=request,
        me=me
    ).handle_request()


@router.delete('/{project_id}/private_keys/{project_private_key_id}', response_model=SuccessResponse)
def delete_project_private_key(
    project_id: int,
    project_private_key_id: int,
    me: User = Depends(auth.get_user)
) -> SuccessResponse:
    return DeleteProjectPrivateKeyController(
        project_id=project_id,
        project_private_key_id=project_private_key_id,
        me=me
    ).handle_request()
