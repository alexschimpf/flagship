import os

from rest_api_tester.runner import TestCaseRunner

from app.constants import UserRole
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestGetUsers(BaseTestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_get_users.json'
        self.runner = TestCaseRunner(
            client=test_client, path_to_scenarios_dir=path_to_scenarios_dir, default_content_type='application/json'
        )
        utils.clear_database()

    def test_get_users__200(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            user = utils.User(projects=[project.project_id])
            with utils.new_user(user=user) as user_row:
                result = self.runner.run(
                    path_to_test_cases=self.path_to_test_cases,
                    test_name='test_get_users__200',
                    response_json_modifiers={
                        'items.[0].user_id': user_row.user_id,
                        'items.[0].created_date': user_row.created_date.isoformat().replace('+00:00', 'Z'),
                        'items.[0].updated_date': user_row.updated_date.isoformat().replace('+00:00', 'Z'),
                        'items.[0].projects': user.projects,
                    },
                    test_data_modifier=self._add_session_cookie(user=user, test_client=self.runner.client),
                )
                self.verify_test_result(result=result)

    def test_get_users__403(self) -> None:
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_get_users__403',
            user=utils.User(role=UserRole.READ_ONLY),
        )
        self.verify_test_result(result=result)
