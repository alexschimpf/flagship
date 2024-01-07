from fastapi import Response
from sqlalchemy import select

from app.api.exceptions.exceptions import UnauthorizedException, CannotDeleteLastOwnerException, NotFoundException
from app.api.schemas import SuccessResponse, User
from app.config import Config
from app.constants import Permission, UserRole
from app.services.database.mysql.schemas.user import UsersTable, UserRow
from app.services.database.mysql.service import MySQLService


class DeleteUserController:

    def __init__(self, user_id: int, me: User):
        self.user_id = user_id
        self.me = me

    def handle_request(self, response: Response) -> SuccessResponse:
        if not self.me.role.has_permission(Permission.DELETE_USER):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            if not session.get(UserRow, self.user_id):
                raise NotFoundException

            user_row = session.scalar(
                select(
                    UserRow.user_id
                ).where(
                    UserRow.role == UserRole.OWNER.value,
                    UserRow.user_id != self.user_id
                ).limit(1)
            )
            if not user_row:
                raise CannotDeleteLastOwnerException

            UsersTable.delete_user(user_id=self.user_id, session=session)
            session.commit()

        if self.user_id == self.me.user_id:
            response.delete_cookie(key=Config.SESSION_COOKIE_KEY)

        return SuccessResponse()
