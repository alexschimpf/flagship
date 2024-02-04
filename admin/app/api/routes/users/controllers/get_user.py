from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.user import UserRow
from app.services.database.mysql.schemas.user_project import UsersProjectsTable
from app.services.database.mysql.service import MySQLService


class GetUserController:

    def __init__(self, user_id: int, me: User):
        self.user_id = user_id
        self.me = me

    def handle_request(self) -> User:
        if self.me.user_id != self.user_id and not self.me.role.has_permission(Permission.READ_USERS):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            user_row = session.get(UserRow, self.user_id)
            projects = UsersProjectsTable.get_user_projects(user_id=self.user_id, session=session)

        if not user_row:
            raise NotFoundException

        return User.from_row(row=user_row, projects=projects)
