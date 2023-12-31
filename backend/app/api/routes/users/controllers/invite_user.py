import secrets

from app.api.routes.users.schemas import InviteUser, User
from app.services.database.mysql.service import MySQLService
from app.services.database.mysql.models.user import UserModel
from app.api.exceptions.exceptions import EmailTakenException, InvalidProjectException
from app.api.routes.users.controllers import common
from app.constants import UserStatus


class InviteUserController:

    def __init__(self, request: InviteUser):
        self.request = request

    def handle_request(self) -> User:
        self._validate()

        user_model = self._create_user()

        return User.from_model(model=user_model)

    def _validate(self) -> None:
        with MySQLService.get_session() as session:
            if UserModel.get_user_by_email(email=self.request.email, session=session):
                raise EmailTakenException(field='email')

        if not common.are_projects_valid(project_ids=self.request.projects):
            raise InvalidProjectException(field='projects')

    def _create_user(self) -> UserModel:
        set_password_token = secrets.token_urlsafe()
        projects = ','.join(map(str, self.request.projects))
        with MySQLService.get_session() as session:
            user_model = UserModel(
                email=self.request.email,
                name=self.request.name,
                role=self.request.role,
                projects=projects,
                status=UserStatus.INVITED.value,
                set_password_token=set_password_token
            )
            session.add(user_model)
            session.commit()
            session.refresh(user_model)

        return user_model
