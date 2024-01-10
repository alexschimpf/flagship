from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field, ConfigDict

from app.services.database.mysql.schemas.project import ProjectRow


class Project(BaseModel):
    project_id: int
    name: str
    created_date: datetime
    updated_date: datetime

    @classmethod
    def from_row(cls, row: ProjectRow) -> Self:
        return cls(
            project_id=row.project_id,
            name=row.name,
            created_date=row.created_date,
            updated_date=row.updated_date
        )


class ProjectWithPrivateKey(Project):
    private_key: str


class Projects(BaseModel):
    items: list[Project]


class CreateOrUpdateProject(BaseModel):
    name: str = Field(min_length=1, max_length=128)

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class ProjectPrivateKey(BaseModel):
    private_key: str


class ProjectPrivateKeyName(BaseModel):
    name: str = Field(min_length=1, max_length=128)

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class ProjectPrivateKeyNameAndId(BaseModel):
    project_private_key_id: int
    name: str


class ProjectPrivateKeys(BaseModel):
    items: list[ProjectPrivateKeyNameAndId]
