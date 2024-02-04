from app.api.routes.feature_flags.schemas import FeatureFlags, FeatureFlag
from app.services.database.mysql.schemas.feature_flag import FeatureFlagsTable
from app.services.database.mysql.service import MySQLService


class GetFeatureFlagsController:

    def __init__(self, project_id: int, page: int, page_size: int) -> None:
        self.project_id = project_id
        self.page = page
        self.page_size = page_size

    def handle_request(self) -> FeatureFlags:
        with MySQLService.get_session() as session:
            feature_flag_rows, total_count = FeatureFlagsTable.get_feature_flags(
                project_id=self.project_id, page=self.page, page_size=self.page_size, session=session
            )

        feature_flags = [
            FeatureFlag.from_row(row=feature_flag_row)
            for feature_flag_row in feature_flag_rows
        ]

        return FeatureFlags(
            items=feature_flags, total=total_count
        )
