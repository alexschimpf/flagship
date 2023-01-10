from typing import Any, Type
from bson import ObjectId
from enum import Enum


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


def get_enum_desc(enum: Type[Enum]) -> str:
    name_to_val = {
        name: val.value
        for name, val in enum.__members__.items()
    }
    description = []
    for name, val in name_to_val.items():
        clean_name = name.lower().replace('_', ' ')
        description.append(f'{clean_name}: {val}')
    return '</br>'.join(description)
