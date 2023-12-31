from app.api.routes.feature_flags.schemas import FeatureFlags, FeatureFlag
from app.services.database.mysql.schemas.feature_flag import FeatureFlagsTable
from app.services.database.mysql.service import MySQLService


class GetFeatureFlagsController:

    def __init__(self, project_id: int) -> None:
        self.project_id = project_id

    def handle_request(self) -> FeatureFlags:
        with MySQLService.get_session() as session:
            feature_flag_rows = FeatureFlagsTable.get_feature_flags(project_id=self.project_id, session=session)

        feature_flags = [
            FeatureFlag.from_row(row=feature_flag_row)
            for feature_flag_row in feature_flag_rows
        ]

        return FeatureFlags(
            items=feature_flags
        )
