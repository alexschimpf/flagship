from typing import Any, cast
from varname import nameof

from app.api import exceptions
from app.api.routes.projects.controllers import common
from app.services.database.mongodb import collections, types
from app.api.routes.projects import schemas


def process(
    request: schemas.CreateOrUpdateProject
) -> Any:
    if collections.projects.is_project_name_taken(name=request.name):
        raise exceptions.NameTakenException(field=nameof(request.name))

    private_key, encrypted_private_key = common.generate_private_key()
    project_id = collections.projects.create_project(
        name=request.name,
        private_key=encrypted_private_key
    )
    project = cast(types.Project, collections.projects.get_project(project_id=project_id))
    return schemas.ProjectWithPrivateKey(
        **project,
        private_key=private_key
    )
