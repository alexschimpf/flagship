import os
import ujson
from typing import Callable, cast
from rest_api_tester.runner import TestCaseRunner
from rest_api_tester.test import TestData

from app.main import app
from app.services.database.mongodb import types

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestSetPassword(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_set_password__200(self) -> None:
        with utils.new_user(
            email='tony.soprano@sopranos.com',
            name='Tony Soprano',
            role=types.UserRole.STANDARD,
            projects=[],
            password_token='token',
            status=types.UserStatus.ACTIVATED
        ):
            result = self.runner.run(
                path_to_test_cases='test_set_password.json',
                test_name='test_set_password__200',
                test_data_modifier=self.modifier(token='token')
            )
            self.verify_test_result(result=result)

    def test_set_password__400_invalid_token(self) -> None:
        with utils.new_user(
            email='tony.soprano@sopranos.com',
            name='Tony Soprano',
            role=types.UserRole.STANDARD,
            projects=[],
            password_token='token',
            status=types.UserStatus.ACTIVATED
        ):
            result = self.runner.run(
                path_to_test_cases='test_set_password.json',
                test_name='test_set_password__400_invalid_token'
            )
            self.verify_test_result(result=result)

    @staticmethod
    def modifier(token: str) -> Callable[[TestData], TestData]:
        def modifier_(test_data: TestData) -> TestData:
            request_data = ujson.loads(cast(str, test_data.request_data))
            request_data['token'] = token
            test_data.request_data = ujson.dumps(request_data)
            return test_data

        return modifier_
