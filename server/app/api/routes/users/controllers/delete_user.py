from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api import schemas, exceptions


def process(
    user_id: str
) -> Any:
    # TODO: What if you're deleting the last admin?

    deleted = collections.users.delete_user(user_id=ObjectId(user_id))
    if not deleted:
        raise exceptions.NotFoundException

    return schemas.SuccessResponse(success=True)
