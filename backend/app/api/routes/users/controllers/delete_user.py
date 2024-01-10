from fastapi import Response

from app.api.exceptions.exceptions import UnauthorizedException, CannotDeleteLastOwnerException, NotFoundException
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
        if not self.me.role.has_permission(Permission.DELETE_USER):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            row = session.get(UserRow, self.user_id)
            if not row:
                raise NotFoundException

            if not UsersTable.owners_exist(excluded_user_id=self.user_id, session=session):
                raise CannotDeleteLastOwnerException

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
