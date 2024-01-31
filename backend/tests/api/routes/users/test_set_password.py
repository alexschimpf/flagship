import os
import time
from typing import Callable

from rest_api_tester.runner import TestCaseRunner
from rest_api_tester.test import TestData

from app.api.routes.users.controllers import common
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
            default_content_type='application/x-www-form-urlencoded'
        )
        utils.clear_database()

    def test_set_password__302_success(self) -> None:
        hashed_set_password_token, token = common.generate_set_password_token()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_success',
            user=utils.User(set_password_token=hashed_set_password_token),
            test_data_modifier=self.add_token(token=token)
        )
        self.verify_test_result(result=result)

        location = result.response.headers['location']
        self.assertEqual(Config.UI_BASE_URL, location)
        set_cookie = result.response.headers['set-cookie']
        self.assertTrue(Config.SESSION_COOKIE_KEY in set_cookie)

    def test_set_password__302_invalid_email(self) -> None:
        hashed_set_password_token, token = common.generate_set_password_token()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_invalid_email',
            user=utils.User(set_password_token=hashed_set_password_token),
            test_data_modifier=self.add_token(token=token, update_header=True)
        )
        self.verify_test_result(result=result)

    def test_set_password__302_invalid_token(self) -> None:
        hashed_set_password_token, _ = common.generate_set_password_token()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_invalid_token',
            user=utils.User(set_password_token=hashed_set_password_token)
        )
        self.verify_test_result(result=result)

    def test_set_password__302_invalid_password(self) -> None:
        hashed_set_password_token, token = common.generate_set_password_token()
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_invalid_password',
            user=utils.User(set_password_token=hashed_set_password_token),
            test_data_modifier=self.add_token(token=token, update_header=True)
        )
        self.verify_test_result(result=result)

    def test_set_password__302_token_expired(self) -> None:
        hashed_set_password_token, token = common.generate_set_password_token()
        hashed_token, _ = hashed_set_password_token.split('|')
        hashed_set_password_token = '|'.join((
            hashed_token,
            str(time.time() - Config.SET_PASSWORD_TOKEN_TTL)
        ))
        result = self.run_test_with_user(
            runner=self.runner,
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_set_password__302_token_expired',
            user=utils.User(set_password_token=hashed_set_password_token),
            test_data_modifier=self.add_token(token=token, update_header=True)
        )
        self.verify_test_result(result=result)

    @staticmethod
    def add_token(token: str, update_header: bool = False) -> Callable[[TestData], TestData]:
        def func(test_data: TestData) -> TestData:
            if test_data.request_data:
                test_data.request_data = test_data.request_data.replace('$$$', token)
            if update_header:
                expected_headers = test_data.expected_headers
                if expected_headers:
                    location_header = expected_headers.get('location')
                    if location_header and 'error' in location_header:
                        expected_headers['location'] = f'{expected_headers['location']}&token={token}'
            return test_data

        return func
