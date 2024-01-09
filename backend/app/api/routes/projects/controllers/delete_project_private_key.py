from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.schemas import SuccessResponse
from app.api.schemas import User
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.project import ProjectRow
from app.services.database.mysql.schemas.project_private_key import ProjectPrivateKeyRow, ProjectPrivateKeysTable
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.service import MySQLService


class DeleteProjectPrivateKeyController:

    def __init__(self, project_id: int, project_private_key_id: int, me: User):
        self.project_id = project_id
        self.project_private_key_id = project_private_key_id
        self.me = me

    def handle_request(self) -> SuccessResponse:
        name = self._validate()
        self._delete_private_key(name=name)

        return SuccessResponse()

    def _validate(self) -> str:
        if (not self.me.role.has_permission(Permission.DELETE_PROJECT_PRIVATE_KEY) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            row = session.get(ProjectRow, self.project_id)
            if not row:
                raise NotFoundException
            if not session.get(ProjectPrivateKeyRow, self.project_private_key_id):
                raise NotFoundException

        return row.name

    def _delete_private_key(self, name: str) -> None:
        with MySQLService.get_session() as session:
            ProjectPrivateKeysTable.delete_project_private_key(
                project_id=self.project_id, project_private_key=self.project_private_key_id, session=session)
            session.add(SystemAuditLogRow(
                actor=self.me.email,
                event_type=AuditLogEventType.DELETED_PROJECT_PRIVATE_KEY,
                details=f'Name: {name}'
            ))
            session.commit()
