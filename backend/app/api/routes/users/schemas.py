from pydantic import BaseModel, EmailStr, Field

from app.api import utils
from app.api.schemas import User
from app.constants import UserRole


class InviteUser(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = Field(description=utils.get_enum_description(enum=UserRole))
    projects: list[int]


class UpdateUser(BaseModel):
    name: str
    role: UserRole = Field(description=utils.get_enum_description(enum=UserRole))
    projects: list[int]


class SetPassword(BaseModel):
    email: str
    password: str
    token: str


class ResetPassword(BaseModel):
    email: EmailStr


class Users(BaseModel):
    items: list[User]
