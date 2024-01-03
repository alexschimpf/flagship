from app.api.exceptions.exceptions import UnauthorizedException
from app.api.schemas import SuccessResponse, User
from app.constants import Permission
from app.services.database.mysql.schemas.user import UsersTable
from app.services.database.mysql.service import MySQLService


class DeleteUserController:

    def __init__(self, user_id: int, me: User):
        self.user_id = user_id
        self.me = me

    def handle_request(self) -> SuccessResponse:
        if not self.me.role.has_permission(Permission.DELETE_USER):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            UsersTable.delete_user(user_id=self.user_id, session=session)
            session.commit()

        return SuccessResponse()
