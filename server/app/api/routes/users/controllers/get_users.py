from typing import Any

from app.services.database.mongodb import collections
from app.api.routes.users import schemas


def process() -> Any:
    return schemas.Users(
        items=collections.users.get_users()
    )
