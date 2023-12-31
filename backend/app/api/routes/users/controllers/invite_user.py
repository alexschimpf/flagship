import secrets

from app.api.exceptions.exceptions import EmailTakenException, InvalidProjectException
from app.api.routes.users.controllers import common
from app.api.routes.users.schemas import InviteUser, User
from app.constants import UserStatus
from app.services.database.mysql.schemas.user import UserRow, UsersTable
from app.services.database.mysql.service import MySQLService


class InviteUserController:

    def __init__(self, request: InviteUser):
        self.request = request

    def handle_request(self) -> User:
        self._validate()

        user_row = self._create_user()

        return User.from_row(row=user_row)

    def _validate(self) -> None:
        with MySQLService.get_session() as session:
            if UsersTable.get_user_by_email(email=self.request.email, session=session):
                raise EmailTakenException(field='email')

        if not common.are_projects_valid(project_ids=self.request.projects):
            raise InvalidProjectException(field='projects')

    def _create_user(self) -> UserRow:
        set_password_token = secrets.token_urlsafe()
        projects = ','.join(map(str, self.request.projects))
        with MySQLService.get_session() as session:
            user_row = UserRow(
                email=self.request.email,
                name=self.request.name,
                role=self.request.role,
                projects=projects,
                status=UserStatus.INVITED.value,
                set_password_token=set_password_token
            )
            session.add(user_row)
            session.commit()
            session.refresh(user_row)

        return user_row
