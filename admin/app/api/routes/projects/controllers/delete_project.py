from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.schemas import SuccessResponse, User
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.project import ProjectsTable, ProjectRow
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.service import MySQLService
from app.services.database.redis.service import RedisService


class DeleteProjectController:
    def __init__(self, project_id: int, me: User):
        self.project_id = project_id
        self.me = me

    def handle_request(self) -> SuccessResponse:
        name = self._validate()
        self._delete_project(name=name)
        return SuccessResponse()

    def _validate(self) -> str:
        if not self.me.role.has_permission(Permission.DELETE_PROJECT) or self.project_id not in self.me.projects:
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            row = session.get(ProjectRow, self.project_id)
            if not row:
                raise NotFoundException

        return row.name

    def _delete_project(self, name: str) -> None:
        with MySQLService.get_session() as session:
            ProjectsTable.delete_project(project_id=self.project_id, session=session)
            session.add(
                SystemAuditLogRow(
                    actor=self.me.email, event_type=AuditLogEventType.DELETED_PROJECT, details=f'Name: {name}'
                )
            )
            session.commit()

        RedisService.remove_project(project_id=self.project_id)
