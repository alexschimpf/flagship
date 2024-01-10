from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.admin.schemas import SystemAuditLog
from app.api.routes.admin.schemas import SystemAuditLogs
from app.api.schemas import User
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogsTable
from app.services.database.mysql.service import MySQLService


class GetAuditLogsController:

    def __init__(self, page: int, page_size: int, me: User):
        self.me = me
        self.page = page
        self.page_size = page_size

    def handle_request(self) -> SystemAuditLogs:
        if not self.me.role.has_permission(Permission.READ_SYSTEM_AUDIT_LOGS):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            rows, total_count = SystemAuditLogsTable.get_system_audit_logs(
                page=self.page, page_size=self.page_size, session=session)

        result = []
        for row in rows:
            event_type = ' '.join([
                word.capitalize() if i == 0 else word.lower()
                for i, word in enumerate(AuditLogEventType(row.event_type).name.split('_'))
            ])
            result.append(
                SystemAuditLog(
                    actor=row.actor,
                    event_time=row.created_date,
                    details=row.details,
                    event_type=event_type
                )
            )

        return SystemAuditLogs(items=result, total=total_count)
