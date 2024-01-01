from typing import cast

from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.users.schemas import User
from app.services.database.mysql.schemas.user import UserRow
from app.services.database.mysql.schemas.user_project import UsersProjectsTable
from app.services.database.mysql.service import MySQLService


class GetUserController:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def handle_request(self) -> User:
        with MySQLService.get_session() as session:
            user_row = session.get(UserRow, self.user_id)
            projects = cast(list[int], UsersProjectsTable.get_user_projects(user_id=self.user_id, session=session))

        if not user_row:
            raise NotFoundException

        return User.from_row(row=user_row, projects=projects)
