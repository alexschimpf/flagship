from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.constants import UserRole, UserStatus
from app.services.database.mysql.schemas.user import UserRow


class ErrorModel(BaseModel):
    code: str
    message: str
    field: str | None


class ErrorResponseModel(BaseModel):
    errors: list[ErrorModel]


class SuccessResponse(BaseModel):
    success: bool = True


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
    def from_row(cls, row: UserRow, projects: list[int]) -> 'User':
        return cls(
            user_id=row.user_id,
            email=row.email,
            name=row.name,
            role=UserRole(row.role),
            status=UserStatus(row.status),
            projects=projects,
            created_date=row.created_date,
            updated_date=row.updated_date
        )
