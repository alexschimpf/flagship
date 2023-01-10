import os
from bson import ObjectId
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from app.services.database.mongodb import collections

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test import TestCase


class TestCreateProject(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_create_project__200(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_create_project.json',
            test_name='test_create_project__200'
        )
        project_id = self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
        try:
            self.verify_test_result(result=result)
        finally:
            if project_id:
                collections.projects.delete_project(project_id=ObjectId(project_id))

    def test_create_project__400_name_taken(self) -> None:
        with utils.new_project(name='Waste Management, Inc.'):
            result = self.runner.run(
                path_to_test_cases='test_create_project.json',
                test_name='test_create_project__400_name_taken'
            )
            self.verify_test_result(result=result)
