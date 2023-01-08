from pydantic import BaseModel
from datetime import datetime
from typing import Any

from app.services.database.mongodb import types


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

    @staticmethod
    def from_raw(raw: types.FeatureFlagCondition) -> 'FeatureFlagCondition':
        return FeatureFlagCondition(
            context_key=raw['context_key'],
            operator=raw['operator'],
            value=raw['value']
        )


class ContextField(BaseModel):
    context_field_id: str
    name: str
    key: str
    value_type: str
    description: str
    created_date: datetime
    updated_date: datetime

    @staticmethod
    def from_raw(raw: types.ContextField) -> 'ContextField':
        return ContextField(
            context_field_id=str(raw['_id']),
            name=raw['name'],
            key=raw['key'],
            value_type=raw['value_type'],
            description=raw['description'],
            created_date=raw['created_date'],
            updated_date=raw['updated_date']
        )


class FeatureFlag(BaseModel):
    feature_flag_id: str
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
    created_date: datetime
    updated_date: datetime

    @staticmethod
    def from_raw(raw: types.FeatureFlag) -> 'FeatureFlag':
        conditions = raw['conditions']
        return FeatureFlag(
            feature_flag_id=str(raw['_id']),
            name=raw['name'],
            description=raw['description'],
            enabled=raw['enabled'],
            conditions=[
                [FeatureFlagCondition.from_raw(raw=condition) for condition in group]
                for group in conditions
            ],
            created_date=raw['created_date'],
            updated_date=raw['updated_date']
        )


class Project(BaseModel):
    project_id: str
    name: str
    created_date: datetime
    updated_date: datetime

    @staticmethod
    def from_raw(raw: types.Project) -> 'Project':
        return Project(
            project_id=str(raw['_id']),
            name=raw['name'],
            created_date=raw['created_date'],
            updated_date=raw['updated_date']
        )


class ProjectFull(Project):
    context_fields: list[ContextField]
    feature_flags: list[FeatureFlag]

    @staticmethod
    def from_raw(raw: types.Project) -> 'ProjectFull':
        return ProjectFull(
            project_id=str(raw['_id']),
            name=raw['name'],
            context_fields=[ContextField.from_raw(raw=item) for item in raw['context_fields']],
            feature_flags=[FeatureFlag.from_raw(raw=item) for item in raw['feature_flags']],
            created_date=raw['created_date'],
            updated_date=raw['updated_date']
        )


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
