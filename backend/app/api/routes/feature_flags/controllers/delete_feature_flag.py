from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.schemas import SuccessResponse, User
from app.constants import Permission
from app.services.database.mysql.schemas.feature_flag import FeatureFlagsTable, FeatureFlagRow
from app.services.database.mysql.service import MySQLService


class DeleteFeatureFlagController:

    def __init__(self, project_id: int, feature_flag_id: int, me: User):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.me = me

    def handle_request(self) -> SuccessResponse:
        self._validate()
        self._delete_feature_flag()
        return SuccessResponse()

    def _validate(self) -> None:
        if not self.me.role.has_permission(Permission.DELETE_FEATURE_FLAG):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            if not session.get(FeatureFlagRow, (self.feature_flag_id, self.project_id)):
                raise NotFoundException

    def _delete_feature_flag(self) -> None:
        with MySQLService.get_session() as session:
            FeatureFlagsTable.delete_feature_flag(
                project_id=self.project_id, feature_flag_id=self.feature_flag_id, session=session
            )
            session.commit()
