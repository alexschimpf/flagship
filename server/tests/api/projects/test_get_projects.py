import os
from rest_api_tester.runner import TestCaseRunner

from app.main import app

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestGetProjects(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_get_projects__200(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_get_projects.json',
                test_name='test_get_projects__200'
            )
            actual_projects = result.response.json()['items']
            self.replace_response_strings(
                result=result,
                id=project_id,
                created_date=actual_projects[0]['created_date'],
                updated_date=actual_projects[0]['updated_date']
            )
            self.verify_test_result(result=result)
