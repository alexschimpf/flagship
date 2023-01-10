from typing import Any

from app.services.database.mongodb import collections
from app.api.routes.projects import schemas


def process() -> Any:
    projects = collections.projects.get_projects()
    return schemas.Projects(
        items=projects
    )
