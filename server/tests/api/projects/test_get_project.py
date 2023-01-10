import os
from bson import ObjectId
from rest_api_tester.runner import TestCaseRunner

from app.main import app

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestGetProject(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_get_project__200(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_get_project.json',
                test_name='test_get_project__200',
                url_params={'project_id': str(project_id)}
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_get_project__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_get_project.json',
            test_name='test_get_project__404',
            url_params={'project_id': str(ObjectId())}
        )
        self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
        self.verify_test_result(result=result)
