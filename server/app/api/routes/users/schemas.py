from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from app.services.database.mongodb import types
from app.api.utils import PydanticObjectId, get_enum_desc


class InviteUser(BaseModel):
    email: EmailStr
    name: str
    role: types.UserRole
    projects: list[str]


class UpdateUser(BaseModel):
    name: str
    role: types.UserRole
    projects: list[str]


class User(BaseModel):
    _id: str | PydanticObjectId = Field(alias='_id')
    email: EmailStr
    name: str
    role: types.UserRole = Field(description=get_enum_desc(types.UserRole))
    projects: list[str]
    status: types.UserStatus = Field(description=get_enum_desc(types.UserStatus))
    created_date: datetime
    updated_date: datetime


class Users(BaseModel):
    items: list[User]
