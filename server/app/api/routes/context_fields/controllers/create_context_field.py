from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api.routes.context_fields import schemas
from app.api import exceptions


def process(
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
