from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.api.utils import PydanticObjectId, get_enum_desc
from app.services.database.mongodb import types


class FeatureFlagCondition(BaseModel):
    context_key: str
    operator: types.Operator = Field(description=get_enum_desc(types.Operator))
    value: Any

    class Config:
        anystr_strip_whitespace = True


class FeatureFlag(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
    created_date: datetime
    updated_date: datetime


class FeatureFlags(BaseModel):
    items: list[FeatureFlag]


class CreateOrUpdateFeatureFlag(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(default='')
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]

    class Config:
        anystr_strip_whitespace = True
