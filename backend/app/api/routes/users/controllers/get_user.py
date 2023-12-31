from app.api.routes.users.schemas import User
from app.services.database.mysql.service import MySQLService
from app.services.database.mysql.models.user import UserModel
from app.api.exceptions.exceptions import NotFoundException


class GetUserController:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def handle_request(self) -> User:
        with MySQLService.get_session() as session:
            user_model = session.get(UserModel, self.user_id)

        if not user_model:
            raise NotFoundException

        return User.from_model(model=user_model)
