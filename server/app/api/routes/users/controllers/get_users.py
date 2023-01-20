from typing import Any

from app.services.database.mongodb import collections


def process() -> Any:
    return collections.users.get_users()
