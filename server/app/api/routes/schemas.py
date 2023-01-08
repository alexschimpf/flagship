from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any
from bson import ObjectId

from app.services.database.mongodb import types


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


class ErrorModel(BaseModel):
    code: str
    message: str
    field: str | None


class ErrorResponseModel(BaseModel):
    errors: list[ErrorModel]


class SuccessResponse(BaseModel):
    success: bool


class FeatureFlagCondition(BaseModel):
    context_key: str
    operator: types.Operator
    value: Any


class ContextField(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    key: str
    value_type: str
    description: str
    created_date: datetime
    updated_date: datetime


class FeatureFlag(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
    created_date: datetime
    updated_date: datetime


class Project(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    created_date: datetime
    updated_date: datetime


class Projects(BaseModel):
    projects: list[Project]


class FeatureFlags(BaseModel):
    feature_flags: list[FeatureFlag]


class ContextFields(BaseModel):
    context_fields: list[ContextField]


class CreateOrUpdateProject(BaseModel):
    name: str


class CreateContextField(BaseModel):
    name: str
    key: str
    value_type: str
    description: str


class UpdateContextField(BaseModel):
    name: str
    description: str


class CreateOrUpdateFeatureFlag(BaseModel):
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
