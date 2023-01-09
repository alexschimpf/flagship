from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.api.utils import PydanticObjectId
from app.services.database.mongodb import types


class FeatureFlagCondition(BaseModel):
    context_key: str
    operator: types.Operator
    value: Any


class FeatureFlag(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
    created_date: datetime
    updated_date: datetime


class FeatureFlags(BaseModel):
    feature_flags: list[FeatureFlag]


class CreateOrUpdateFeatureFlag(BaseModel):
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
