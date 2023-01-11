from typing import Any
from bson import ObjectId
from varname import nameof

from app.services.database.mongodb import collections, types
from app.api.routes.context_fields import schemas
from app.api.routes.context_fields.controllers import common
from app.api import exceptions


def process(
    project_id: str,
    request: schemas.CreateContextField
) -> Any:
    errors: list[exceptions.AppException] = []
    _validate_name(project_id=project_id, request=request, errors=errors)
    _validate_key(project_id=project_id, request=request, errors=errors)
    _validate_enum_type(request=request, errors=errors)
    common.validate_enum_def(request=request, errors=errors)

    if errors:
        raise exceptions.AggregateException(exceptions=errors)

    context_field_id, project_found = collections.projects.create_context_field(
        project_id=ObjectId(project_id),
        name=request.name,
        key=request.key,
        value_type=request.value_type,
        description=request.description,
        enum_def=request.enum_def
    )
    if not project_found:
        raise exceptions.NotFoundException

    return collections.projects.get_context_field(
        project_id=ObjectId(project_id), context_field_id=context_field_id
    )


def _validate_name(
    project_id: str,
    request: schemas.CreateContextField,
    errors: list[exceptions.AppException]
) -> None:
    if collections.projects.is_context_field_name_taken(
        project_id=ObjectId(project_id),
        name=request.name
    ):
        errors.append(exceptions.NameTakenException(field=nameof(request.name)))


def _validate_key(
    project_id: str,
    request: schemas.CreateContextField,
    errors: list[exceptions.AppException]
) -> None:
    if collections.projects.is_context_field_key_taken(
        project_id=ObjectId(project_id),
        key=request.key
    ):
        errors.append(exceptions.ContextFieldKeyTakenException(field=nameof(request.key)))


def _validate_enum_type(
    request: schemas.CreateContextField,
    errors: list[exceptions.AppException]
) -> None:
    if (
        request.value_type in (types.ContextValueType.ENUM, types.ContextValueType.ENUM_LIST) and
        not request.enum_def
    ):
        errors.append(exceptions.EnumContextFieldTypeWithoutEnumDefException(nameof(request.enum_def)))

    if (
        request.value_type not in (types.ContextValueType.ENUM, types.ContextValueType.ENUM_LIST) and
        request.enum_def
    ):
        # Clear this field, since it isn't applicable for non-enum types
        request.enum_def = None
