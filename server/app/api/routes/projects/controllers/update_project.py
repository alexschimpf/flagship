from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api.routes.projects import schemas
from app.api import exceptions


def process(
    project_id: str,
    request: schemas.CreateOrUpdateProject
) -> Any:
    matched = collections.projects.update_project(project_id=ObjectId(project_id), name=request.name)
    if not matched:
        raise exceptions.NotFoundException

    return collections.projects.get_project(project_id=ObjectId(project_id))
