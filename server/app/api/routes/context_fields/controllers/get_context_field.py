from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api import exceptions


def process(
    project_id: str,
    context_field_id: str
) -> Any:
    context_field = collections.projects.get_context_field(
        project_id=ObjectId(project_id), context_field_id=ObjectId(context_field_id)
    )
    if not context_field:
        raise exceptions.NotFoundException

    return context_field
