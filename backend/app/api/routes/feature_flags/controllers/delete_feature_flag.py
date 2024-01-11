from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.schemas import SuccessResponse, User
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.feature_flag import FeatureFlagsTable, FeatureFlagRow
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.service import MySQLService


class DeleteFeatureFlagController:

    def __init__(self, project_id: int, feature_flag_id: int, me: User):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.me = me

    def handle_request(self) -> SuccessResponse:
        name = self._validate()
        self._delete_feature_flag(name=name)
        return SuccessResponse()

    def _validate(self) -> str:
        if (not self.me.role.has_permission(Permission.DELETE_FEATURE_FLAG)
                or self.project_id not in self.me.projects):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            row = session.get(FeatureFlagRow, self.feature_flag_id)
            if not row:
                raise NotFoundException

        return row.name

    def _delete_feature_flag(self, name: str) -> None:
        with MySQLService.get_session() as session:
            FeatureFlagsTable.delete_feature_flag(
                project_id=self.project_id, feature_flag_id=self.feature_flag_id, session=session
            )
            session.add(SystemAuditLogRow(
                actor=self.me.email,
                event_type=AuditLogEventType.DELETED_FEATURE_FLAG,
                details=f'Name: {name}'
            ))
            session.commit()
