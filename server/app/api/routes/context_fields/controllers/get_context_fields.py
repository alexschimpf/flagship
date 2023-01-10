from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api.routes.context_fields import schemas
from app.api import exceptions


def process(
    project_id: str
) -> Any:
    context_fields = collections.projects.get_context_fields(project_id=ObjectId(project_id))
    if context_fields is None:
        raise exceptions.NotFoundException

    return schemas.ContextFields(items=context_fields)
