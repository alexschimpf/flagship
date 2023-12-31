from typing import Any, Self
from datetime import datetime
from pydantic import BaseModel, Field

from app import constants
from app.services.database.mysql.models.feature_flag import FeatureFlagModel


class FeatureFlagCondition(BaseModel):
    context_key: str
    operator: constants.Operator
    value: Any

    class Config:
        str_strip_whitespace = True


class FeatureFlag(BaseModel):
    feature_flag_id: int
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
    created_date: datetime
    updated_date: datetime

    @classmethod
    def from_model(cls, model: FeatureFlagModel) -> Self:
        return cls(
            feature_flag_id=model.feature_flag_id,
            name=model.name,
            description=model.description,
            enabled=model.enabled,
            conditions=model.conditions_json,
            created_date=model.created_date,
            updated_date=model.updated_date
        )


class FeatureFlags(BaseModel):
    items: list[FeatureFlag]


class CreateOrUpdateFeatureFlag(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str = Field(default='', max_length=256)
    enabled: bool
    conditions: list[list[FeatureFlagCondition]] = Field(default=[])

    class Config:
        str_strip_whitespace = True
