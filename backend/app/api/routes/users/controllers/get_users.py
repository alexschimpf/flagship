from collections import defaultdict

from sqlalchemy import select

from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.users.schemas import Users
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.user import UsersTable
from app.services.database.mysql.schemas.user_project import UserProjectRow
from app.services.database.mysql.service import MySQLService


class GetUsersController:

    def __init__(self, me: User) -> None:
        self.me = me

    def handle_request(self) -> Users:
        if not self.me.role.has_permission(Permission.READ_USERS):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            user_rows = UsersTable.get_users(session=session)
            all_user_projects = session.scalars(
                select(
                    UserProjectRow
                )
            )
            projects_by_user: dict[int, list[int]] = defaultdict(list)
            for user_project_row in all_user_projects:
                projects_by_user[user_project_row.user_id].append(user_project_row.project_id)

        users = [
            User.from_row(
                row=user_row,
                projects=projects_by_user[user_row.user_id]
            ) for user_row in user_rows
        ]

        return Users(
            items=users
        )
