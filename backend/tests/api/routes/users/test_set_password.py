import os
import secrets

from rest_api_tester.runner import TestCaseRunner

from app.config import Config
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestSetPassword(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_set_password.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_set_password__302_success(self) -> None:
        set_password_token = secrets.token_urlsafe()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_success',
            user=utils.User(set_password_token=set_password_token),
            request_json_modifiers={
                'token': set_password_token
            }
        )
        self.verify_test_result(result=result)

        location = result.response.headers['location']
        self.assertEqual(Config.UI_BASE_URL, location)
        set_cookie = result.response.headers['set-cookie']
        self.assertTrue(Config.SESSION_COOKIE_KEY in set_cookie)

    def test_set_password__302_invalid_email(self) -> None:
        set_password_token = secrets.token_urlsafe()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_invalid_email',
            user=utils.User(set_password_token=set_password_token),
            request_json_modifiers={
                'token': set_password_token
            }
        )
        self.verify_test_result(result=result)

    def test_set_password__302_invalid_token(self) -> None:
        set_password_token = secrets.token_urlsafe()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_invalid_token',
            user=utils.User(set_password_token=set_password_token)
        )
        self.verify_test_result(result=result)

    def test_set_password__302_invalid_password(self) -> None:
        set_password_token = secrets.token_urlsafe()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_invalid_password',
            user=utils.User(set_password_token=set_password_token),
            request_json_modifiers={
                'token': set_password_token
            }
        )
        self.verify_test_result(result=result)
