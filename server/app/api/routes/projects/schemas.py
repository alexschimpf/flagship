from datetime import datetime
from pydantic import BaseModel, Field

from app.api.utils import PydanticObjectId


class Project(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    created_date: datetime
    updated_date: datetime


class Projects(BaseModel):
    projects: list[Project]


class CreateOrUpdateProject(BaseModel):
    name: str
