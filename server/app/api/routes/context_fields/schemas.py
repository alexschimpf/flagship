from datetime import datetime
from pydantic import BaseModel, Field

from app.api.utils import PydanticObjectId


class ContextField(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    key: str
    value_type: str
    description: str
    created_date: datetime
    updated_date: datetime


class ContextFields(BaseModel):
    items: list[ContextField]


class CreateContextField(BaseModel):
    name: str
    key: str
    value_type: str
    description: str


class UpdateContextField(BaseModel):
    name: str
    description: str
