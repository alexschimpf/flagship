import os

from rest_api_tester.runner import TestCaseRunner

from app.config import Config
from app.constants import UserRole
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestDeleteUser(BaseTestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_delete_user.json'
        self.runner = TestCaseRunner(
            client=test_client, path_to_scenarios_dir=path_to_scenarios_dir, default_content_type='application/json'
        )
        utils.clear_database()

    def test_delete_user__200(self) -> None:
        with utils.new_user(user=utils.User(email='test@test.com')) as user:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_delete_user__200',
                user=utils.User(),
                url_params={'user_id': user.user_id},
            )
            self.verify_test_result(result=result)

    def test_delete_user__200_delete_myself(self) -> None:
        user = utils.User()
        with utils.new_user(user=utils.User(email='test@test.com')), utils.new_user(user=user) as user_row:
            result = self.runner.run(
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_delete_user__200_delete_myself',
                url_params={'user_id': user_row.user_id},
                test_data_modifier=self._add_session_cookie(user=user, test_client=self.runner.client),
            )
            self.verify_test_result(result=result)

            set_cookie = result.response.headers['set-cookie']
            self.assertTrue(Config.SESSION_COOKIE_KEY in set_cookie and 'expires' in set_cookie)

    def test_delete_user__403_read_only_role(self) -> None:
        with utils.new_user(user=utils.User(email='test@test.com')) as user:
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_delete_user__403_read_only_role',
                user=utils.User(role=UserRole.READ_ONLY),
                url_params={'user_id': user.user_id},
            )
            self.verify_test_result(result=result)

    def test_delete_user__400_no_owners_left(self) -> None:
        user = utils.User()
        with utils.new_user(user=utils.User()) as user_row:
            result = self.runner.run(
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_delete_user__400_no_owners_left',
                url_params={'user_id': user_row.user_id},
                test_data_modifier=self._add_session_cookie(user=user, test_client=self.runner.client),
            )
            self.verify_test_result(result=result)

    def test_delete_user__404(self) -> None:
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_delete_user__404',
            user=utils.User(),
            url_params={'user_id': 999},
        )
        self.verify_test_result(result=result)
