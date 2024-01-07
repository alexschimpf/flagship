import os
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from app.constants import UserRole
from tests.api.fastapi_test_client import FastAPITestClient
from tests.api.base_test_case import BaseTestCase
from tests.api import utils


class TestCreateProject(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.owner_user = utils.User()
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_create_project.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_create_project__200(self) -> None:
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_create_project__200',
            user=self.owner_user
        )
        self.verify_test_result(
            result=result,
            excluded_response_paths=[
                'created_date', 'updated_date', 'private_key', 'project_id'
            ]
        )

    def test_create_project__400_name_too_long(self) -> None:
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_create_project__400_name_too_long',
            user=self.owner_user
        )
        self.verify_test_result(result=result)

    def test_create_project__400_name_taken(self) -> None:
        with utils.new_project(project=utils.Project()):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_create_project__400_name_taken',
                user=self.owner_user
            )
            self.verify_test_result(result=result)

    def test_create_project__401(self) -> None:
        standard_user = utils.User(role=UserRole.STANDARD)
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_create_project__401',
            user=standard_user
        )
        self.verify_test_result(result=result)
