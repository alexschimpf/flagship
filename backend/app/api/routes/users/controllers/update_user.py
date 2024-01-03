from typing import cast

from app.api.exceptions.exceptions import InvalidProjectException, NotFoundException, NoProjectAssignedException, \
    UnauthorizedException
from app.api.routes.users.schemas import UpdateUser
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.project import ProjectsTable
from app.services.database.mysql.schemas.user import UserRow, UsersTable
from app.services.database.mysql.schemas.user_project import UsersProjectsTable
from app.services.database.mysql.service import MySQLService


class UpdateUserController:

    def __init__(self, user_id: int, request: UpdateUser, me: User):
        self.user_id = user_id
        self.request = request
        self.me = me

    def handle_request(self) -> User:
        self._validate()
        user_row = self._update_user()

        return User.from_row(row=user_row, projects=self.request.projects)

    def _validate(self) -> None:
        if self.me.user_id != self.user_id and not self.me.role.has_permission(Permission.UPDATE_USER):
            raise UnauthorizedException

        if not self.request.projects:
            raise NoProjectAssignedException(field='projects')

        with MySQLService.get_session() as session:
            if not session.get(UserRow, self.user_id):
                raise NotFoundException

            if not ProjectsTable.are_projects_valid(project_ids=self.request.projects, session=session):
                raise InvalidProjectException(field='projects')

    def _update_user(self) -> UserRow:
        with MySQLService.get_session() as session:
            UsersTable.update_user(
                user_id=self.user_id,
                name=self.request.name,
                role=self.request.role,
                session=session
            )

            UsersProjectsTable.update_user_projects(
                user_id=self.user_id, project_ids=self.request.projects, session=session)

            session.commit()

            user_row = session.get(UserRow, self.user_id)

        return cast(UserRow, user_row)
