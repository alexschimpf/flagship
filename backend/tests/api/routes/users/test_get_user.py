import os

from rest_api_tester.runner import TestCaseRunner

from app.constants import UserRole
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestGetUser(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_get_user.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_get_user__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_user(user=utils.User(email='test@test.com', projects=[project.project_id])) as user
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_get_user__200',
                user=utils.User(),
                url_params={'user_id': user.user_id},
                response_json_modifiers={
                    'user_id': user.user_id,
                    'created_date': user.created_date.isoformat(),
                    'updated_date': user.updated_date.isoformat(),
                    'projects': [project.project_id]
                }
            )
            self.verify_test_result(result=result)

    def test_get_user__403(self) -> None:
        with utils.new_user(user=utils.User(email='test@test.com')) as user:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_get_user__403',
                user=utils.User(role=UserRole.READ_ONLY),
                url_params={'user_id': user.user_id}
            )
            self.verify_test_result(result=result)

    def test_get_user__404(self) -> None:
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_get_user__404',
            user=utils.User()
        )
        self.verify_test_result(result=result)
