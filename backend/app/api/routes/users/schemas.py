from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.constants import UserRole, UserStatus
from app.services.database.mysql.schemas.user import UserRow


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
    def from_row(cls, row: UserRow) -> 'User':
        return cls(
            user_id=row.user_id,
            email=row.email,
            name=row.name,
            role=UserRole(row.role),
            projects=row.projects_list,
            status=UserStatus(row.status),
            created_date=row.created_date,
            updated_date=row.updated_date
        )


class Users(BaseModel):
    items: list[User]
