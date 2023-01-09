from typing import Any
from fastapi import APIRouter

from app.api.routes.context_fields import schemas
from app.api.schemas import SuccessResponse
from app.api.routes.context_fields import controllers

router = APIRouter(
    prefix='/context-fields',
    tags=['Context Fields']
)


@router.get('', response_model=schemas.ContextFields)
def get_context_fields(
    project_id: str
) -> Any:
    return controllers.get_context_fields.process(project_id=project_id)


@router.post('', response_model=schemas.ContextField)
def create_context_field(
    project_id: str,
    request: schemas.CreateContextField
) -> Any:
    return controllers.create_context_field.process(
        project_id=project_id, request=request)


@router.get('/{context_field_id}', response_model=schemas.ContextField)
def get_context_field(
    project_id: str,
    context_field_id: str
) -> Any:
    return controllers.get_context_field.process(
        project_id=project_id, context_field_id=context_field_id)


@router.put('/{context_field_id}', response_model=schemas.ContextField)
def update_context_field(
    project_id: str,
    context_field_id: str,
    request: schemas.UpdateContextField
) -> Any:
    return controllers.update_context_field.process(
        project_id=project_id, context_field_id=context_field_id, request=request)


@router.delete('/{context_field_id}', response_model=SuccessResponse)
def delete_context_field(
    project_id: str,
    context_field_id: str
) -> Any:
    return controllers.delete_context_field.process(
        project_id=project_id, context_field_id=context_field_id)
