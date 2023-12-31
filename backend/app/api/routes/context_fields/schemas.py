from typing import Any, Self
from datetime import datetime
from pydantic import BaseModel, Field

from app.constants import ContextValueType
from app.services.database.mysql.models.context_field import ContextFieldModel


class ContextField(BaseModel):
    context_field_id: int
    name: str
    field_key: str
    value_type: ContextValueType
    description: str
    enum_def: dict[str, Any] | None
    created_date: datetime
    updated_date: datetime

    @classmethod
    def from_model(cls, model: ContextFieldModel) -> Self:
        return cls(
            context_field_id=model.context_field_id,
            name=model.name,
            field_key=model.field_key,
            value_type=model.value_type,
            description=model.description,
            enum_def=model.enum_def_json,
            created_date=model.created_date,
            updated_date=model.updated_date
        )


class ContextFields(BaseModel):
    items: list[ContextField]


class CreateContextField(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    field_key: str = Field(min_length=1, max_length=64)
    value_type: ContextValueType
    description: str = Field(default='', max_length=256)
    enum_def: dict[str, Any] | None = None

    class Config:
        str_strip_whitespace = True


class UpdateContextField(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str = Field(default='', max_length=256)
    enum_def: dict[str, Any] | None = None

    class Config:
        str_strip_whitespace = True
