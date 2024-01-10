from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.routes.feature_flags.schemas import UpdateFeatureFlagStatus
from app.api.schemas import SuccessResponse, User
from app.constants import Permission
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow, FeatureFlagsTable
from app.services.database.mysql.schemas.feature_flag_audit_logs import FeatureFlagAuditLogRow
from app.services.database.mysql.service import MySQLService


class UpdateFeatureFlagStatusController:

    def __init__(self, project_id: int, feature_flag_id: int, request: UpdateFeatureFlagStatus, me: User):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.request = request
        self.me = me

    def handle_request(self) -> SuccessResponse:
        if (not self.me.role.has_permission(Permission.UPDATE_FEATURE_FLAG) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            row = session.get(FeatureFlagRow, (self.feature_flag_id, self.project_id))
            if not row:
                raise NotFoundException

            FeatureFlagsTable.update_feature_flag_status(
                project_id=self.project_id, feature_flag_id=self.feature_flag_id,
                enabled=self.request.enabled, session=session)
            session.add(FeatureFlagAuditLogRow(
                feature_flag_id=self.feature_flag_id,
                project_id=self.project_id,
                actor=self.me.email,
                name=row.name,
                description=row.description,
                conditions=row.conditions,
                enabled=self.request.enabled
            ))
            session.commit()

        return SuccessResponse()
