from typing import Any, cast
from bson import ObjectId

from app.api.routes.projects.controllers import common
from app.services.database.mongodb import collections, types
from app.api.routes.projects import schemas
from app.api import exceptions


def process(
    project_id: str
) -> Any:
    private_key, encrypted_private_key = common.generate_private_key()

    matched = collections.projects.update_project(
        project_id=ObjectId(project_id),
        private_key=encrypted_private_key
    )
    if not matched:
        raise exceptions.NotFoundException

    project = cast(types.Project, collections.projects.get_project(project_id=ObjectId(project_id)))
    return schemas.ProjectWithPrivateKey(
        **project,
        private_key=private_key
    )
