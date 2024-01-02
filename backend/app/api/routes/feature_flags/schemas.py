from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.api import utils
from app.constants import Operator
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow


class FeatureFlagCondition(BaseModel):
    context_key: str
    operator: Operator = Field(description=utils.get_enum_description(enum=Operator))
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
    def from_row(cls, row: FeatureFlagRow) -> 'FeatureFlag':
        # TODO: Fix conditions
        return cls(
            feature_flag_id=row.feature_flag_id,
            name=row.name,
            description=row.description,
            enabled=row.enabled,
            conditions=row.conditions_json,  # type: ignore
            created_date=row.created_date,
            updated_date=row.updated_date
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
