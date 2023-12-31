from app.api.exceptions.exceptions import InvalidProjectException, NotFoundException
from app.api.routes.users.controllers import common
from app.api.routes.users.schemas import UpdateUser, User
from app.services.database.mysql.schemas.user import UserRow, UsersTable
from app.services.database.mysql.service import MySQLService


class UpdateUserController:

    def __init__(self, user_id: int, request: UpdateUser):
        self.user_id = user_id
        self.request = request

    def handle_request(self) -> User:
        self._validate()

        user_row = self._update_user()
        if not user_row:
            raise NotFoundException

        return User.from_row(row=user_row)

    def _validate(self) -> None:
        if not common.are_projects_valid(project_ids=self.request.projects):
            raise InvalidProjectException(field='projects')

    def _update_user(self) -> UserRow | None:
        projects = ','.join(map(str, self.request.projects))
        with MySQLService.get_session() as session:
            UsersTable.update_user(
                user_id=self.user_id,
                name=self.request.name,
                role=self.request.role,
                projects=projects,
                session=session
            )
            session.commit()

            user_row = session.get(UserRow, self.user_id)

        return user_row
