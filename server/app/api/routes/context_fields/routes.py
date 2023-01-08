from typing import Any
from fastapi import APIRouter
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api.routes import schemas
from app.api import exceptions

router = APIRouter(
    prefix='/context-fields',
    tags=['Context Fields']
)


@router.get('', response_model=schemas.ContextFields)
async def get_context_fields(
    project_id: str
) -> Any:
    context_fields = collections.projects.get_context_fields(project_id=ObjectId(project_id))
    if context_fields is None:
        raise exceptions.NotFoundException

    return schemas.ContextFields(context_fields=context_fields)


@router.post('', response_model=schemas.ContextField)
async def create_context_field(
    project_id: str,
    request: schemas.CreateContextField
) -> Any:
    context_field_id, project_found = collections.projects.create_context_field(
        project_id=ObjectId(project_id),
        name=request.name,
        key=request.key,
        value_type=request.value_type,
        description=request.description
    )
    if not project_found:
        raise exceptions.NotFoundException

    return collections.projects.get_context_field(
        project_id=ObjectId(project_id), context_field_id=context_field_id
    )


@router.get('/{context_field_id}', response_model=schemas.ContextField)
async def get_context_field(
    project_id: str,
    context_field_id: str
) -> Any:
    context_field = collections.projects.get_context_field(
        project_id=ObjectId(project_id), context_field_id=ObjectId(context_field_id)
    )
    if not context_field:
        raise exceptions.NotFoundException

    return context_field


@router.put('/{context_field_id}', response_model=schemas.ContextField)
async def update_context_field(
    project_id: str,
    context_field_id: str,
    request: schemas.UpdateContextField
) -> Any:
    matched = collections.projects.update_context_field(
        project_id=ObjectId(project_id),
        context_field_id=ObjectId(context_field_id),
        name=request.name,
        description=request.description
    )
    if not matched:
        raise exceptions.NotFoundException

    return collections.projects.get_context_field(
        project_id=ObjectId(project_id), context_field_id=ObjectId(context_field_id)
    )


@router.delete('/{context_field_id}', response_model=schemas.SuccessResponse)
async def delete_context_field(
    project_id: str,
    context_field_id: str
) -> Any:
    deleted = collections.projects.delete_context_field(
        project_id=ObjectId(project_id),
        context_field_id=ObjectId(context_field_id)
    )
    if not deleted:
        raise exceptions.NotFoundException

    return schemas.SuccessResponse(success=True)
