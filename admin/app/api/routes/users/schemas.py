from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.api.schemas import User
from app.constants import UserRole


class InviteUser(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=128)
    role: UserRole
    projects: list[int]

    model_config = ConfigDict(str_strip_whitespace=True)


class UpdateUser(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    role: UserRole
    projects: list[int]

    model_config = ConfigDict(str_strip_whitespace=True)


class SetPassword(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str
    token: str


class ResetPassword(BaseModel):
    email: EmailStr


class Users(BaseModel):
    items: list[User]
    total: int
