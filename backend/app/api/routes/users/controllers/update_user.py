from typing import cast
from sqlalchemy.orm import Session

from app.api.exceptions.exceptions import InvalidProjectException, NotFoundException, NoProjectAssignedException, \
    UnauthorizedException, NoOwnersLeftException
from app.api.routes.users.schemas import UpdateUser
from app.api.schemas import User
from app.constants import Permission, AuditLogEventType, UserRole
from app.services.database.mysql.schemas.project import ProjectsTable
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.schemas.user import UserRow, UsersTable
from app.services.database.mysql.schemas.user_project import UsersProjectsTable
from app.services.database.mysql.service import MySQLService


class UpdateUserController:

    def __init__(self, user_id: int, request: UpdateUser, me: User):
        self.user_id = user_id
        self.request = request
        self.me = me

    def handle_request(self) -> User:
        email = self._validate()
        user_row = self._update_user(email=email)

        return User.from_row(row=user_row, projects=self.request.projects)

    def _validate(self) -> str:
        is_updating_me = self.me.user_id == self.user_id

        if not is_updating_me and not self.me.role.has_permission(Permission.UPDATE_USER):
            raise UnauthorizedException

        if not self.request.projects:
            raise NoProjectAssignedException(field='projects')

        with MySQLService.get_session() as session:
            row = session.get(UserRow, self.user_id)
            if not row:
                raise NotFoundException

            projects = UsersProjectsTable.get_user_projects(user_id=self.user_id, session=session)

            if not ProjectsTable.are_projects_valid(project_ids=self.request.projects, session=session):
                raise InvalidProjectException(field='projects')

            self._validate_role_and_projects(user_row=row, projects=projects, session=session)

        return row.email

    def _validate_role_and_projects(self, user_row: UserRow, projects: list[int], session: Session) -> None:
        if (
            (
                not self.me.role.has_permission(Permission.UPDATE_USER_ROLE) and
                self.request.role != user_row.role
            ) or
            (
                not self.me.role.has_permission(Permission.UPDATE_USER_PROJECTS) and
                self.request.projects != projects
            )
        ):
            raise UnauthorizedException

        if (
            user_row.role == UserRole.OWNER and
            self.request.role != UserRole.OWNER and
            not UsersTable.owners_exist(excluded_user_id=self.user_id, session=session)
        ):
            raise NoOwnersLeftException

    def _update_user(self, email: str) -> UserRow:
        with MySQLService.get_session() as session:
            UsersTable.update_user(
                user_id=self.user_id,
                name=self.request.name,
                role=self.request.role,
                session=session
            )

            UsersProjectsTable.update_user_projects(
                user_id=self.user_id, project_ids=self.request.projects, session=session)

            session.add(SystemAuditLogRow(
                actor=self.me.email,
                event_type=AuditLogEventType.UPDATED_USER,
                details=f'Email: {email}'
            ))

            session.commit()

            user_row = session.get(UserRow, self.user_id)

        return cast(UserRow, user_row)
