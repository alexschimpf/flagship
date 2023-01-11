from typing import Any
from bson import ObjectId
from varname import nameof

from app.services.database.mongodb import collections, types
from app.api.routes.context_fields import schemas
from app.api.routes.context_fields.controllers import common
from app.api import exceptions


def process(
    project_id: str,
    context_field_id: str,
    request: schemas.UpdateContextField
) -> Any:
    existing_context_field = _validate_exists(project_id=project_id, context_field_id=context_field_id)

    errors: list[exceptions.AppException] = []
    _validate_name(project_id=project_id, context_field_id=context_field_id, request=request, errors=errors)
    _validate_enum_type(request=request, existing=existing_context_field, errors=errors)
    common.validate_enum_def(request=request, errors=errors)

    if errors:
        raise exceptions.AggregateException(exceptions=errors)

    collections.projects.update_context_field(
        project_id=ObjectId(project_id),
        context_field_id=ObjectId(context_field_id),
        name=request.name,
        description=request.description,
        enum_def=request.enum_def
    )

    return collections.projects.get_context_field(
        project_id=ObjectId(project_id), context_field_id=ObjectId(context_field_id)
    )


def _validate_exists(
    project_id: str,
    context_field_id: str
) -> types.ContextField:
    context_field = collections.projects.get_context_field(
        project_id=ObjectId(project_id),
        context_field_id=ObjectId(context_field_id)
    )
    if not context_field:
        raise exceptions.NotFoundException

    return context_field


def _validate_name(
    project_id: str,
    context_field_id: str,
    request: schemas.UpdateContextField,
    errors: list[exceptions.AppException]
) -> None:
    if collections.projects.is_context_field_name_taken(
        project_id=ObjectId(project_id),
        name=request.name,
        exclude_context_field_id=ObjectId(context_field_id)
    ):
        errors.append(exceptions.NameTakenException(field=nameof(request.name)))


def _validate_enum_type(
    request: schemas.UpdateContextField,
    existing: types.ContextField,
    errors: list[exceptions.AppException]
) -> None:
    if (
        existing['value_type'] in (types.ContextValueType.ENUM, types.ContextValueType.ENUM_LIST) and
        not request.enum_def
    ):
        errors.append(exceptions.EnumContextFieldTypeWithoutEnumDefException(nameof(request.enum_def)))

    if (
        existing['value_type'] not in (types.ContextValueType.ENUM, types.ContextValueType.ENUM_LIST) and
        request.enum_def
    ):
        # Clear this field, since it isn't applicable for non-enum types
        request.enum_def = None
