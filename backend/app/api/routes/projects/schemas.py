from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from app.services.database.mysql.models.project import ProjectModel


class Project(BaseModel):
    project_id: int
    name: str
    created_date: datetime
    updated_date: datetime

    @classmethod
    def from_model(cls, model: ProjectModel) -> Self:
        return cls(
            project_id=model.project_id,
            name=model.name,
            created_date=model.created_date,
            updated_date=model.updated_date
        )


class ProjectWithPrivateKey(Project):
    private_key: str


class Projects(BaseModel):
    items: list[Project]


class CreateOrUpdateProject(BaseModel):
    name: str = Field(min_length=1, max_length=128)

    class Config:
        str_strip_whitespace = True
