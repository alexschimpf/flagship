from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.feature_flags.schemas import FeatureFlag
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow
from app.services.database.mysql.service import MySQLService


class GetFeatureFlagController:

    def __init__(self, project_id: int, feature_flag_id: int):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id

    def handle_request(self) -> FeatureFlag:
        with MySQLService.get_session() as session:
            feature_flag_row = session.get(FeatureFlagRow, self.feature_flag_id)

        if not feature_flag_row:
            raise NotFoundException

        return FeatureFlag.from_row(row=feature_flag_row)
