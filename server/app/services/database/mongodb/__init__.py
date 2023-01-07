from typing import Any, cast
from pymongo import MongoClient
from pymongo.collection import Collection

from app.services.database.mongodb import types
from app.config import MONGODB_CONN_STR


class MongoDBService:

    _client: MongoClient[dict[str, Any]]

    @classmethod
    def init(cls) -> None:
        cls._client = MongoClient(
            host=MONGODB_CONN_STR,
            connect=True
        )

    @classmethod
    def projects(cls) -> Collection[types.Project]:
        return cast(Collection[types.Project], cls._client.flagship.projects)
