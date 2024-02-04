from fastapi import Response

from app.api.exceptions.exceptions import UnauthorizedException, NoOwnersLeftException, NotFoundException
from app.api.schemas import SuccessResponse, User
from app.config import Config
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.schemas.user import UsersTable, UserRow
from app.services.database.mysql.service import MySQLService


class DeleteUserController:

    def __init__(self, user_id: int, me: User):
        self.user_id = user_id
        self.me = me

    def handle_request(self, response: Response) -> SuccessResponse:
        with MySQLService.get_session() as session:
            row = session.get(UserRow, self.user_id)
            if not row:
                raise NotFoundException

            # Don't allow a user to delete another user with a higher role
            if not self.me.role.has_permission(Permission.DELETE_USER) or row.role > self.me.role:
                raise UnauthorizedException

            if not UsersTable.owners_exist(excluded_user_id=self.user_id, session=session):
                raise NoOwnersLeftException

            UsersTable.delete_user(user_id=self.user_id, session=session)

            session.add(SystemAuditLogRow(
                actor=self.me.email,
                event_type=AuditLogEventType.DELETED_USER,
                details=f'Email: {row.email}'
            ))

            session.commit()

        if self.user_id == self.me.user_id:
            response.delete_cookie(key=Config.SESSION_COOKIE_KEY)

        return SuccessResponse()
