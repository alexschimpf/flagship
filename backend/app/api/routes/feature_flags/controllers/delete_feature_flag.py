from app.services.database.mysql.service import MySQLService
from app.services.database.mysql.models.feature_flag import FeatureFlagModel
from app.api.schemas import SuccessResponse


class DeleteFeatureFlagController:

    def __init__(self, project_id: int, feature_flag_id: int):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id

    def handle_request(self) -> SuccessResponse:
        self._delete_feature_flag()
        return SuccessResponse()

    def _delete_feature_flag(self) -> None:
        with MySQLService.get_session() as session:
            FeatureFlagModel.delete_feature_flag(
                project_id=self.project_id, feature_flag_id=self.feature_flag_id, session=session
            )
            session.commit()
