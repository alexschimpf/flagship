from typing import Any
from bson import ObjectId
from varname import nameof

from app.services.database.mongodb import collections
from app.api.routes.context_fields import schemas
from app.api import exceptions


def process(
    project_id: str,
    context_field_id: str,
    request: schemas.UpdateContextField
) -> Any:
    if not collections.projects.get_context_field(
        project_id=ObjectId(project_id),
        context_field_id=ObjectId(context_field_id)
    ):
        raise exceptions.NotFoundException

    if collections.projects.is_context_field_name_taken(
        project_id=ObjectId(project_id),
        name=request.name,
        exclude_context_field_id=ObjectId(context_field_id)
    ):
        raise exceptions.NameTakenException(field=nameof(request.name))

    collections.projects.update_context_field(
        project_id=ObjectId(project_id),
        context_field_id=ObjectId(context_field_id),
        name=request.name,
        description=request.description
    )

    return collections.projects.get_context_field(
        project_id=ObjectId(project_id), context_field_id=ObjectId(context_field_id)
    )
