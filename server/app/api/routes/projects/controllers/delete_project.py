from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api.schemas import SuccessResponse
from app.api import exceptions


def process(
    project_id: str
) -> Any:
    deleted = collections.projects.delete_project(project_id=ObjectId(project_id))
    if not deleted:
        raise exceptions.NotFoundException

    return SuccessResponse(success=True)
