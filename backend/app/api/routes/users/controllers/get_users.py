from app.api.routes.users.schemas import Users, User
from app.services.database.mysql.schemas.user import UsersTable
from app.services.database.mysql.service import MySQLService


class GetUsersController:

    def __init__(self) -> None:
        pass

    @staticmethod
    def handle_request() -> Users:
        # TODO: Protect this endpoint
        with MySQLService.get_session() as session:
            user_rows = UsersTable.get_users(session=session)

        users = [
            User.from_row(row=user_row)
            for user_row in user_rows
        ]

        return Users(
            items=users
        )
