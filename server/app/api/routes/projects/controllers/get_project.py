from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api import exceptions


def process(
    project_id: str
) -> Any:
    project = collections.projects.get_project(project_id=ObjectId(project_id))
    if not project:
        raise exceptions.NotFoundException

    return project
