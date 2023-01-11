from datetime import datetime
from pydantic import BaseModel, Field

from app.api.utils import PydanticObjectId, get_enum_desc
from app.services.database.mongodb.types import ContextValueType


class ContextField(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    key: str
    value_type: ContextValueType
    description: str
    created_date: datetime
    updated_date: datetime


class ContextFields(BaseModel):
    items: list[ContextField]


class CreateContextField(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    key: str = Field(min_length=1, max_length=32)
    value_type: ContextValueType = Field(description=get_enum_desc(ContextValueType))
    description: str = Field(default='')

    class Config:
        anystr_strip_whitespace = True


class UpdateContextField(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str = Field(default='', max_length=256)

    class Config:
        anystr_strip_whitespace = True
