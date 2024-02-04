import os

from rest_api_tester.runner import TestCaseRunner

from app.constants import UserRole
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestDeleteProject(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_delete_project.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_delete_project__200(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_delete_project__200',
                user=utils.User(projects=[project.project_id]),
                url_params={'project_id': project.project_id}
            )
            self.verify_test_result(result=result)

    def test_delete_project__401(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_delete_project__401',
                user=utils.User(role=UserRole.STANDARD),
                url_params={'project_id': project.project_id}
            )
            self.verify_test_result(result=result)
