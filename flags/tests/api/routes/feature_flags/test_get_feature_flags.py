import os
import hmac
import hashlib

from rest_api_tester.runner import TestCaseRunner
from rest_api_tester.test import TestCase

from app.main import app
from tests.api.fastapi_test_client import FastAPITestClient


class TestGetFeatureFlags(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_get_feature_flags.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        self.private_key = '5c18cf7802ac166fcd610c5b7fd24015a417fc110a07dc295e90fd7dce0fd0a3'

    def test_get_feature_flags__200(self) -> None:
        signature = self._generate_signature(
            private_key=self.private_key,
            user_key='1'
        )
        result = self.runner.run(
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_get_feature_flags__200',
            url_params={
                'project_id': 1,
                'user_key': 1
            },
            request_header_modifiers={
                'FLAGSHIP-SIGNATURE': signature
            }
        )
        self.verify_test_result(result=result)

    def test_get_feature_flags__200_no_flags(self) -> None:
        signature = self._generate_signature(
            private_key=self.private_key,
            user_key='1'
        )
        result = self.runner.run(
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_get_feature_flags__200_no_flags',
            url_params={
                'project_id': 1,
                'user_key': 1
            },
            request_header_modifiers={
                'FLAGSHIP-SIGNATURE': signature
            }
        )
        self.verify_test_result(result=result)

    def test_get_feature_flags__403(self) -> None:
        result = self.runner.run(
            path_to_test_cases=self.path_to_test_cases,
            test_name='test_get_feature_flags__403',
            url_params={
                'project_id': 1,
                'user_key': 1
            }
        )
        self.verify_test_result(result=result)

    @staticmethod
    def _generate_signature(private_key: str, user_key: str) -> str:
        return hmac.new(
            private_key.encode(),
            user_key.encode(),
            hashlib.sha256
        ).hexdigest()
