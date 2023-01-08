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
    def from_doc(doc: types.FeatureFlagCondition) -> 'FeatureFlagCondition':
        return FeatureFlagCondition(
            context_key=doc['context_key'],
            operator=doc['operator'],
            value=doc['value']
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
    def from_doc(doc: types.ContextField) -> 'ContextField':
        return ContextField(
            context_field_id=str(doc['_id']),
            name=doc['name'],
            key=doc['key'],
            value_type=doc['value_type'],
            description=doc['description'],
            created_date=doc['created_date'],
            updated_date=doc['updated_date']
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
    def from_doc(doc: types.FeatureFlag) -> 'FeatureFlag':
        conditions = doc['conditions']
        return FeatureFlag(
            feature_flag_id=str(doc['_id']),
            name=doc['name'],
            description=doc['description'],
            enabled=doc['enabled'],
            conditions=[
                [FeatureFlagCondition.from_doc(doc=condition) for condition in group]
                for group in conditions
            ],
            created_date=doc['created_date'],
            updated_date=doc['updated_date']
        )


class Project(BaseModel):
    project_id: str
    name: str
    created_date: datetime
    updated_date: datetime

    @staticmethod
    def from_doc(doc: types.Project) -> 'Project':
        return Project(
            project_id=str(doc['_id']),
            name=doc['name'],
            created_date=doc['created_date'],
            updated_date=doc['updated_date']
        )


class ProjectFull(Project):
    context_fields: list[ContextField]
    feature_flags: list[FeatureFlag]

    @staticmethod
    def from_doc(doc: types.Project) -> 'ProjectFull':
        return ProjectFull(
            project_id=str(doc['_id']),
            name=doc['name'],
            context_fields=[ContextField.from_doc(doc=item) for item in doc['context_fields']],
            feature_flags=[FeatureFlag.from_doc(doc=item) for item in doc['feature_flags']],
            created_date=doc['created_date'],
            updated_date=doc['updated_date']
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
