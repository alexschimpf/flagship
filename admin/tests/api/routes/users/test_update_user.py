import os

from rest_api_tester.runner import TestCaseRunner

from app.constants import UserRole
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestUpdateUser(BaseTestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_update_user.json'
        self.runner = TestCaseRunner(
            client=test_client, path_to_scenarios_dir=path_to_scenarios_dir, default_content_type='application/json'
        )
        utils.clear_database()

    def test_update_user__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_user(user=utils.User(email='test@test.com', projects=[project.project_id])) as user,
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_user__200',
                user=utils.User(),
                url_params={'user_id': user.user_id},
                request_json_modifiers={'projects': [project.project_id]},
                response_json_modifiers={
                    'user_id': user.user_id,
                    'created_date': user.created_date.isoformat().replace('+00:00', 'Z'),
                    'projects': [project.project_id],
                },
            )
            self.verify_test_result(result=result, excluded_response_paths=['updated_date'])

    def test_update_user__403(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_user(user=utils.User(email='test@test.com', projects=[project.project_id])) as user,
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_user__403',
                user=utils.User(role=UserRole.READ_ONLY),
                url_params={'user_id': user.user_id},
                request_json_modifiers={'projects': [project.project_id]},
            )
            self.verify_test_result(result=result)

    def test_update_user__400_no_project_assigned(self) -> None:
        with utils.new_user(user=utils.User(email='test@test.com')) as user:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_user__400_no_project_assigned',
                user=utils.User(),
                url_params={'user_id': user.user_id},
            )
            self.verify_test_result(result=result)

    def test_update_user__400_invalid_project(self) -> None:
        with utils.new_user(user=utils.User(email='test@test.com')) as user:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_user__400_invalid_project',
                user=utils.User(),
                url_params={'user_id': user.user_id},
            )
            self.verify_test_result(result=result)

    def test_update_user__404(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_user(user=utils.User(email='test@test.com', projects=[project.project_id])) as user,
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_user__404',
                user=utils.User(),
                url_params={'user_id': user.user_id},
                request_json_modifiers={'projects': [project.project_id]},
            )
            self.verify_test_result(result=result)
