import os

from rest_api_tester.runner import TestCaseRunner

from app.main import app
from app.services.database.mysql.schemas.user import UserRow
from app.services.database.mysql.service import MySQLService
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestResetPassword(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(
            os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_reset_password.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_reset_password__200(self) -> None:
        with utils.new_user(user=utils.User()) as user:
            with MySQLService.get_session() as session:
                user_row_before = session.get(UserRow, user.user_id)
                if user_row_before:
                    self.assertIsNone(user_row_before.set_password_token)

            result = self.runner.run(
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_reset_password__200'
            )
            self.verify_test_result(result=result)

            with MySQLService.get_session() as session:
                user_row = session.get(UserRow, user.user_id)
                if user_row:
                    self.assertIsNotNone(user_row.set_password_token)
