import os
import ujson
from bson import ObjectId
from typing import cast, Callable
from rest_api_tester.runner import TestCaseRunner
from rest_api_tester.test import TestData

from app.main import app
from app.services.database.mongodb import types

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestUpdateUser(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_update_user__200(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_user(
                email='tony.soprano@sopranos.com',
                name='Tony Soprano',
                role=types.UserRole.STANDARD,
                projects=[],
                password_token='token',
                status=types.UserStatus.ACTIVATED
            ) as user_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_update_user.json',
                test_name='test_update_user__200',
                url_params={
                    'user_id': str(user_id)
                },
                test_data_modifier=self.modifier(projects=[str(project_id)])
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_update_user__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_update_user.json',
            test_name='test_update_user__404',
            url_params={
                'user_id': ObjectId()
            }
        )
        self.verify_test_result(result=result)

    @staticmethod
    def modifier(projects: list[str]) -> Callable[[TestData], TestData]:
        def modifier_(test_data: TestData) -> TestData:
            request_data = ujson.loads(cast(str, test_data.request_data))
            request_data['projects'] = projects
            test_data.request_data = ujson.dumps(request_data)

            expected_response = ujson.loads(cast(str, test_data.expected_response))
            expected_response['projects'] = projects
            test_data.expected_response = ujson.dumps(expected_response)

            return test_data

        return modifier_
