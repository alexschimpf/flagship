from datetime import datetime
from pydantic import BaseModel, Field

from app.api.utils import PydanticObjectId


class Project(BaseModel):
    id_: str | PydanticObjectId = Field(alias='_id')
    name: str
    created_date: datetime
    updated_date: datetime


class Projects(BaseModel):
    items: list[Project]


class CreateOrUpdateProject(BaseModel):
    name: str = Field(min_length=1)

    class Config:
        anystr_strip_whitespace = True
