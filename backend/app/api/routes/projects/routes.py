from typing import Any
from fastapi import APIRouter

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.get('')
def get_projects() -> Any:
    pass


@router.post('')
def create_project() -> Any:
    pass


@router.get('/{project_id}')
def get_project(project_id: str) -> Any:
    pass


@router.put('/{project_id}')
def update_project(project_id: str, request: Any) -> Any:
    pass


@router.delete('/{project_id}')
def delete_project(project_id: str) -> Any:
    pass


@router.post('/{project_id}/private_key')
def reset_project_private_key(project_id: str) -> Any:
    pass
