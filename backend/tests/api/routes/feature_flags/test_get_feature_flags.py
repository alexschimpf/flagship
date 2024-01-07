import os

from rest_api_tester.runner import TestCaseRunner

from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestGetFeatureFlags(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_get_feature_flags.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_get_feature_flags__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project1,
            utils.new_project(project=utils.Project(name='other')) as project2,
            utils.new_feature_flag(
                project_id=project1.project_id, feature_flag=utils.FeatureFlag()) as feature_flag1,
            utils.new_feature_flag(
                project_id=project2.project_id, feature_flag=utils.FeatureFlag()),
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_get_feature_flags__200',
                user=utils.User(projects=[project1.project_id]),
                url_params={
                    'project_id': project1.project_id,
                    'feature_flag_id': feature_flag1.feature_flag_id
                },
                response_json_modifiers={
                    'items.[0].feature_flag_id': feature_flag1.feature_flag_id,
                    'items.[0].updated_date': feature_flag1.updated_date.isoformat(),
                    'items.[0].created_date': feature_flag1.created_date.isoformat()
                }
            )
            self.verify_test_result(result=result)
