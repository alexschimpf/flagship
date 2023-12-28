from typing import Any
from fastapi import APIRouter

router = APIRouter(
    prefix='/context_fields',
    tags=['Context Fields']
)


@router.get('')
def get_context_fields(project_id: str) -> Any:
    pass


@router.post('')
def create_context_field(project_id: str, request: Any) -> Any:
    pass


@router.get('/{context_field_id}')
def get_context_field(project_id: str, context_field_id: str) -> Any:
    pass


@router.put('/{context_field_id}')
def update_context_field(project_id: str, context_field_id: str, request: Any) -> Any:
    pass


@router.delete('/{context_field_id}')
def delete_context_field(project_id: str, context_field_id: str) -> Any:
    pass
