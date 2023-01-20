import os
from bson import ObjectId
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from app.services.database.mongodb import types

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestDeleteUser(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_delete_user__200(self) -> None:
        with utils.new_user(
                email='tony.soprano@sopranos.com',
                name='Tony Soprano',
                role=types.UserRole.STANDARD,
                projects=[],
                password_token='token',
                status=types.UserStatus.ACTIVATED
        ) as user_id:
            result = self.runner.run(
                path_to_test_cases='test_delete_user.json',
                test_name='test_delete_user__200',
                url_params={
                    'user_id': user_id
                }
            )
            self.verify_test_result(result=result)

    def test_delete_user__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_get_user.json',
            test_name='test_get_user__404',
            url_params={
                'user_id': ObjectId()
            }
        )
        self.verify_test_result(result=result)
