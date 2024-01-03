from fastapi import APIRouter, Depends

from app.api import auth
from app.api.routes.projects.controllers.create_project import CreateProjectController
from app.api.routes.projects.controllers.delete_project import DeleteProjectController
from app.api.routes.projects.controllers.get_project import GetProjectController
from app.api.routes.projects.controllers.get_projects import GetProjectsController
from app.api.routes.projects.controllers.reset_project_private_key import ResetProjectPrivateKeyController
from app.api.routes.projects.controllers.update_project import UpdateProjectController
from app.api.routes.projects.schemas import Project, Projects, CreateOrUpdateProject, ProjectWithPrivateKey
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


@router.post('/{project_id}/private_key', response_model=ProjectWithPrivateKey)
def reset_project_private_key(
    project_id: int,
    me: User = Depends(auth.get_user)
) -> ProjectWithPrivateKey:
    return ResetProjectPrivateKeyController(
        project_id=project_id,
        me=me
    ).handle_request()
