from typing import Any
from varname import nameof

from app.api import exceptions
from app.services.database.mongodb import collections
from app.api.routes.projects import schemas


def process(
    request: schemas.CreateOrUpdateProject
) -> Any:
    if collections.projects.is_project_name_taken(name=request.name):
        raise exceptions.NameTakenException(field=nameof(request.name))

    project_id = collections.projects.create_project(name=request.name)
    return collections.projects.get_project(project_id=project_id)
