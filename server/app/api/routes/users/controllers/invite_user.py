from typing import Any
import secrets
from bson import ObjectId

from app.services.database.mongodb import types, collections
from app.api.routes.users import schemas


def process(
    request: schemas.InviteUser
) -> Any:
    password_token = secrets.token_urlsafe()
    user_id = collections.users.create_user(
        email=request.email,
        name=request.name,
        role=request.role,
        projects=list(map(ObjectId, request.projects)),
        password_token=password_token,
        status=types.UserStatus.INVITED
    )

    # TODO: Send invite email

    return collections.users.get_user(user_id=user_id)
