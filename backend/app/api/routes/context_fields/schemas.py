from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel, Field, ConfigDict

from app.api import utils
from app.constants import ContextValueType
from app.services.database.mysql.schemas.context_field import ContextFieldRow


class ContextField(BaseModel):
    context_field_id: int
    name: str
    field_key: str
    value_type: ContextValueType = Field(description=utils.get_enum_description(enum=ContextValueType))
    description: str
    enum_def: dict[str, Any] | None
    created_date: datetime
    updated_date: datetime

    @classmethod
    def from_row(cls, row: ContextFieldRow) -> Self:
        return cls(
            context_field_id=row.context_field_id,
            name=row.name,
            field_key=row.field_key,
            value_type=ContextValueType(row.value_type),
            description=row.description,
            enum_def=row.enum_def_dict,
            created_date=row.created_date,
            updated_date=row.updated_date
        )


class ContextFields(BaseModel):
    items: list[ContextField]


class CreateContextField(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    field_key: str = Field(min_length=1, max_length=64)
    value_type: ContextValueType = Field(description=utils.get_enum_description(enum=ContextValueType))
    description: str = Field(default='', max_length=256)
    enum_def: dict[str, Any] | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class UpdateContextField(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str = Field(default='', max_length=256)
    enum_def: dict[str, Any] | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True
    )
