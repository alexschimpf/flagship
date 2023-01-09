from typing import Any

from app.services.database.mongodb import collections
from app.api.routes.projects import schemas


def process(
    request: schemas.CreateOrUpdateProject
) -> Any:
    project_id = collections.projects.create_project(name=request.name)
    return collections.projects.get_project(project_id=project_id)
