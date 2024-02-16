from typing import Any, Callable, cast

import ujson
from rest_api_tester.client.base_client import BaseTestClient
from rest_api_tester.runner import TestCaseRunner
from rest_api_tester.test import TestCase, TestResult, TestData

from app.config import Config
from tests.api import utils


class BaseTestCase(TestCase):

    def run_test_with_user(
        self,
        runner: TestCaseRunner,
        path_to_test_cases: str,
        test_name: str,
        user: utils.User,
        url_params: dict[str, Any] | None = None,
        test_data_modifier: Callable[[TestData], TestData] | None = None,
        request_json_modifiers: dict[str, Any] | None = None,
        response_json_modifiers: dict[str, Any] | None = None
    ) -> TestResult:
        with utils.new_user(user=user):
            return runner.run(
                path_to_test_cases=path_to_test_cases,
                test_name=test_name,
                test_data_modifier=self._add_session_cookie(
                    user=user, test_client=runner.client, test_data_modifier=test_data_modifier),
                url_params=url_params,
                request_json_modifiers=request_json_modifiers,
                response_json_modifiers=response_json_modifiers
            )

    @classmethod
    def _add_session_cookie(
        cls,
        user: utils.User,
        test_client: BaseTestClient,
        test_data_modifier: Callable[[TestData], TestData] | None = None
    ) -> Callable[[TestData], TestData]:
        def func(test_data: TestData) -> TestData:
            if test_data_modifier:
                test_data = test_data_modifier(test_data)

            session_cookie = cls._login(
                email=user.email, password=user.password, test_client=test_client)
            if test_data.cookies is None:
                test_data.cookies = {}
            test_data.cookies[Config.SESSION_COOKIE_KEY] = session_cookie
            return test_data

        return func

    @staticmethod
    def _login(email: str, password: str, test_client: BaseTestClient) -> str:
        form_data = '&'.join((f'email={email}', f'password={password}'))
        resp = test_client.post(
            url='/auth/login',
            allow_redirects=False,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=form_data,
            timeout=5
        )

        if resp.status_code != 302:
            raise AssertionError(f'Failed to login: {ujson.dumps(resp.json)}')

        cookie = resp.headers.get('set-cookie')
        if not cookie:
            raise AssertionError('Session cookie missing from login response')

        session_cookie = cookie.split(';')[0]
        if not session_cookie:
            raise AssertionError('Session cookie missing from login response')

        return cast(str, session_cookie.split('=')[1])
