from fastapi import APIRouter, Depends

from app.api import auth
from app.api.routes.context_fields.controllers.create_context_field import CreateContextFieldController
from app.api.routes.context_fields.controllers.delete_context_field import DeleteContextFieldController
from app.api.routes.context_fields.controllers.get_context_field import GetContextFieldController
from app.api.routes.context_fields.controllers.get_context_fields import GetContextFieldsController
from app.api.routes.context_fields.controllers.update_context_field import UpdateContextFieldController
from app.api.routes.context_fields.schemas import CreateContextField, UpdateContextField, ContextField, ContextFields
from app.api.schemas import SuccessResponse, User

router = APIRouter(
    prefix='/context_fields',
    tags=['Context Fields']
)


@router.get('', response_model=ContextFields)
def get_context_fields(project_id: int) -> ContextFields:
    return GetContextFieldsController(
        project_id=project_id
    ).handle_request()


@router.post('', response_model=ContextField)
def create_context_field(
    project_id: int,
    request: CreateContextField,
    me: User = Depends(auth.get_user)
) -> ContextField:
    return CreateContextFieldController(
        project_id=project_id,
        request=request,
        me=me
    ).handle_request()


@router.get('/{context_field_id}', response_model=ContextField)
def get_context_field(project_id: int, context_field_id: int) -> ContextField:
    return GetContextFieldController(
        project_id=project_id,
        context_field_id=context_field_id
    ).handle_request()


@router.put('/{context_field_id}', response_model=ContextField)
def update_context_field(
    project_id: int,
    context_field_id: int,
    request: UpdateContextField,
    me: User = Depends(auth.get_user)
) -> ContextField:
    return UpdateContextFieldController(
        project_id=project_id,
        context_field_id=context_field_id,
        request=request,
        me=me
    ).handle_request()


@router.delete('/{context_field_id}', response_model=SuccessResponse)
def delete_context_field(
    project_id: int,
    context_field_id: int,
    me: User = Depends(auth.get_user)
) -> SuccessResponse:
    return DeleteContextFieldController(
        project_id=project_id,
        context_field_id=context_field_id,
        me=me
    ).handle_request()
