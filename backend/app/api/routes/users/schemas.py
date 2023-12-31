from typing import Self
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.constants import UserRole, UserStatus
from app.services.database.mysql.models.user import UserModel


class InviteUser(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    projects: list[int]


class UpdateUser(BaseModel):
    name: str
    role: UserRole
    projects: list[int]


class SetPassword(BaseModel):
    email: str
    password: str
    token: str


class ResetPassword(BaseModel):
    email: EmailStr


class User(BaseModel):
    user_id: int
    email: EmailStr
    name: str
    role: UserRole
    projects: list[int]
    status: UserStatus
    created_date: datetime
    updated_date: datetime

    @classmethod
    def from_model(cls, model: UserModel) -> Self:
        return cls(
            user_id=model.user_id,
            email=model.email,
            name=model.name,
            role=model.role,
            projects=model.projects_list,
            status=model.status,
            created_date=model.created_date,
            updated_date=model.updated_date
        )


class Users(BaseModel):
    items: list[User]
