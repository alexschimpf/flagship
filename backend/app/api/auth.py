from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT

from app.api.schemas import User
from app.services.database.mysql.schemas.user import UserRow
from app.services.database.mysql.schemas.user_project import UsersProjectsTable
from app.services.database.mysql.service import MySQLService


def get_user(authorize: AuthJWT = Depends()) -> User:
    authorize.jwt_required()

    user_id = int(authorize.get_jwt_subject())

    with MySQLService.get_session() as session:
        user_row = session.get(UserRow, user_id)
        if not user_row:
            raise Exception('Session user not found')

        projects = UsersProjectsTable.get_user_projects(user_id=user_id, session=session)

    return User.from_row(row=user_row, projects=projects)

