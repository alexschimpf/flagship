from app.api.exceptions.exceptions import InvalidProjectException, NotFoundException
from app.api.routes.users.controllers import common
from app.api.routes.users.schemas import UpdateUser, User
from app.services.database.mysql.models.user import UserModel
from app.services.database.mysql.service import MySQLService


class UpdateUserController:

    def __init__(self, user_id: int, request: UpdateUser):
        self.user_id = user_id
        self.request = request

    def handle_request(self) -> User:
        self._validate()

        user_model = self._update_user()
        if not user_model:
            raise NotFoundException

        return User.from_model(model=user_model)

    def _validate(self) -> None:
        if not common.are_projects_valid(project_ids=self.request.projects):
            raise InvalidProjectException(field='projects')

    def _update_user(self) -> UserModel | None:
        projects = ','.join(map(str, self.request.projects))
        with MySQLService.get_session() as session:
            UserModel.update_user(
                user_id=self.user_id,
                name=self.request.name,
                role=self.request.role,
                projects=projects,
                session=session
            )
            session.commit()

            user_model = session.get(UserModel, self.user_id)

        return user_model
