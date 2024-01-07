import os
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from tests.api.fastapi_test_client import FastAPITestClient
from tests.api.base_test_case import BaseTestCase
from tests.api import utils
from app.config import Config
from app.constants import UserStatus


class TestLogin(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_login.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/x-www-form-urlencoded',
        )
        utils.clear_database()

    def test_login__302_success(self) -> None:
        with utils.new_user(user=utils.User()):
            result = self.runner.run(
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_login__302_success'
            )
            self.verify_test_result(result=result)

            location = result.response.headers['location']
            self.assertEqual(Config.UI_BASE_URL, location)
            set_cookie = result.response.headers['set-cookie']
            self.assertTrue(Config.SESSION_COOKIE_KEY in set_cookie)

    def test_login__302_user_not_activated(self) -> None:
        with utils.new_user(user=utils.User(status=UserStatus.INVITED)):
            result = self.runner.run(
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_login__302_user_not_activated'
            )
            self.verify_test_result(result=result)

    def test_login__302_invalid_credentials(self) -> None:
        with utils.new_user(user=utils.User()):
            result = self.runner.run(
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_login__302_invalid_credentials'
            )
            self.verify_test_result(result=result)
