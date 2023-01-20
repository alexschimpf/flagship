from typing import Any
import secrets
from varname import nameof
from bson import ObjectId

from app.services.database.mongodb import types, collections
from app.api.routes.users import schemas
from app.api import exceptions


def process(
    request: schemas.InviteUser
) -> Any:
    _validate_projects(request=request)

    password_token = secrets.token_urlsafe()
    user_id = collections.users.create_user(
        email=request.email,
        name=request.name,
        role=request.role,
        projects=[ObjectId(project_id) for project_id in request.projects],
        password_token=password_token,
        status=types.UserStatus.INVITED
    )

    # TODO: Send invite email

    return collections.users.get_user(user_id=user_id)


def _validate_projects(request: schemas.InviteUser) -> None:
    actual_projects = {
        str(p['_id']) for p in collections.projects.get_projects()
    }
    for project in request.projects:
        if project not in actual_projects:
            raise exceptions.InvalidProjectException(field=nameof(request.projects))
