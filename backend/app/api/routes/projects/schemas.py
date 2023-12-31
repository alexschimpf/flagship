from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

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

    class Config:
        str_strip_whitespace = True
