from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api.routes.users import schemas
from app.api import exceptions


def process(
    user_id: str,
    request: schemas.UpdateUser
) -> Any:
    user_found = collections.users.update_user(
        user_id=ObjectId(user_id),
        name=request.name,
        role=request.role,
        projects=list(map(ObjectId, request.projects))
    )
    if not user_found:
        raise exceptions.NotFoundException

    # TODO: What if user hasn't been activated?

    return collections.users.get_user(user_id=ObjectId(user_id))
