import os

from rest_api_tester.runner import TestCaseRunner

from app.constants import UserRole
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestUpdateFeatureFlagStatus(BaseTestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_update_feature_flag_status.json'
        self.runner = TestCaseRunner(
            client=test_client, path_to_scenarios_dir=path_to_scenarios_dir, default_content_type='application/json'
        )
        utils.clear_database()

    def test_update_feature_flag_status__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_feature_flag(project_id=project.project_id, feature_flag=utils.FeatureFlag()) as feature_flag,
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_feature_flag_status__200',
                user=utils.User(projects=[project.project_id]),
                url_params={'project_id': project.project_id, 'feature_flag_id': feature_flag.feature_flag_id},
            )
            self.verify_test_result(result=result)

    def test_update_feature_flag_status__403_project_not_assigned(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_feature_flag(project_id=project.project_id, feature_flag=utils.FeatureFlag()) as feature_flag,
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_feature_flag_status__403_project_not_assigned',
                user=utils.User(),
                url_params={'project_id': project.project_id, 'feature_flag_id': feature_flag.feature_flag_id},
            )
            self.verify_test_result(result=result)

    def test_update_feature_flag_status__403_read_only_role(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_feature_flag(project_id=project.project_id, feature_flag=utils.FeatureFlag()) as feature_flag,
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_feature_flag_status__403_read_only_role',
                user=utils.User(projects=[project.project_id], role=UserRole.READ_ONLY),
                url_params={'project_id': project.project_id, 'feature_flag_id': feature_flag.feature_flag_id},
            )
            self.verify_test_result(result=result)

    def test_update_feature_flag_status__404(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_feature_flag_status__404',
                user=utils.User(projects=[project.project_id]),
                url_params={'project_id': project.project_id},
            )
            self.verify_test_result(result=result)
