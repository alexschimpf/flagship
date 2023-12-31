from app.api.schemas import SuccessResponse
from app.services.database.mysql.schemas.user import UsersTable
from app.services.database.mysql.service import MySQLService


class DeleteUserController:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def handle_request(self) -> SuccessResponse:
        with MySQLService.get_session() as session:
            UsersTable.delete_user(user_id=self.user_id, session=session)
            session.commit()

        return SuccessResponse()
