from app.api.routes.users.schemas import Users, User
from app.services.database.mysql.models.user import UserModel
from app.services.database.mysql.service import MySQLService


class GetUsersController:

    def __init__(self) -> None:
        pass

    @staticmethod
    def handle_request() -> Users:
        # TODO: Protect this endpoint
        with MySQLService.get_session() as session:
            user_models = UserModel.get_users(session=session)

        users = [
            User.from_model(model=user_model)
            for user_model in user_models
        ]

        return Users(
            items=users
        )
