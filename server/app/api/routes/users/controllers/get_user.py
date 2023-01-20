from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api import exceptions


def process(
    user_id: str
) -> Any:
    user = collections.users.get_user(user_id=ObjectId(user_id))
    if not user:
        raise exceptions.NotFoundException

    return user
