from typing import Any
from bson import ObjectId


class PydanticObjectId(ObjectId):

    @classmethod
    def validate(cls, v: Any) -> str:
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict[Any, Any]) -> None:
        field_schema.update(type='string')
