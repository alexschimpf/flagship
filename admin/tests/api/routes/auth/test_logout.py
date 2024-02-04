import os

from rest_api_tester.runner import TestCaseRunner

from app.config import Config
from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestLogout(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_logout.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_logout__302(self) -> None:
        result = self.runner.run(
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_logout__302'
        )
        self.verify_test_result(result=result)

        set_cookie = result.response.headers['set-cookie']
        self.assertTrue(Config.SESSION_COOKIE_KEY in set_cookie and 'expires' in set_cookie)
