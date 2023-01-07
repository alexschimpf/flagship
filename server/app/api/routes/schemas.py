from pydantic import BaseModel
from datetime import datetime

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
    pass


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

    @staticmethod
    def from_raw(raw: types.FeatureFlag) -> 'FeatureFlag':
        return FeatureFlag()


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
