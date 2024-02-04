from app.api.exceptions.exceptions import EmailTakenException, InvalidProjectException, NoProjectAssignedException, \
    UnauthorizedException
from app.api.routes.users.controllers import common
from app.api.routes.users.schemas import InviteUser
from app.api.schemas import User
from app.constants import Permission, UserStatus, AuditLogEventType
from app.services.database.mysql.schemas.project import ProjectsTable
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.schemas.user import UserRow, UsersTable
from app.services.database.mysql.schemas.user_project import UsersProjectsTable
from app.services.database.mysql.service import MySQLService


class InviteUserController:

    def __init__(self, request: InviteUser, me: User):
        self.request = request
        self.me = me

    def handle_request(self) -> User:
        self._validate()

        hashed_set_password_token, token = common.generate_set_password_token()
        user_row = self._create_user(set_password_token=hashed_set_password_token)

        # TODO: Send invite/set password email (using token)

        return User.from_row(row=user_row, projects=self.request.projects)

    def _validate(self) -> None:
        # Don't allow a user to create/invite another user with a higher role
        if not self.me.role.has_permission(Permission.INVITE_USER) or self.request.role > self.me.role:
            raise UnauthorizedException

        if not self.request.projects:
            raise NoProjectAssignedException(field='projects')

        with MySQLService.get_session() as session:
            if UsersTable.get_user_by_email(email=self.request.email, session=session):
                raise EmailTakenException(field='email')

            if not ProjectsTable.are_projects_valid(project_ids=self.request.projects, session=session):
                raise InvalidProjectException(field='projects')

    def _create_user(self, set_password_token: str) -> UserRow:
        with MySQLService.get_session() as session:
            user_row = UserRow(
                email=self.request.email,
                name=self.request.name,
                role=self.request.role,
                status=UserStatus.INVITED,
                set_password_token=set_password_token
            )
            session.add(user_row)
            session.flush()

            UsersProjectsTable.update_user_projects(
                user_id=user_row.user_id, project_ids=self.request.projects, session=session)

            session.add(SystemAuditLogRow(
                actor=self.me.email,
                event_type=AuditLogEventType.INVITED_USER,
                details=f'Email: {user_row.email}'
            ))

            session.commit()
            session.refresh(user_row)

        return user_row
