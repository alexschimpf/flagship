import os
from bson import ObjectId
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from app.services.database.mongodb import collections

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test import TestCase


class TestProjects(TestCase):

    DEFAULT_IGNORE_FIELDS = ('_id', 'created_date', 'updated_date')

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

    def test_update_project__200(self) -> None:
        with utils.new_project(name='Gabagool Industries') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_update_project.json',
                test_name='test_update_project__200',
                url_params={'project_id': str(project_id)}
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_update_project__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_update_project.json',
            test_name='test_update_project__404',
            url_params={'project_id': str(ObjectId())}
        )
        self.verify_test_result(result=result)

    def test_delete_project__200(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_delete_project.json',
                test_name='test_delete_project__200',
                url_params={'project_id': str(project_id)}
            )
            self.verify_test_result(result=result)

    def test_delete_project__404(self) -> None:
        result = self.runner.run(
            path_to_test_cases='test_delete_project.json',
            test_name='test_delete_project__404',
            url_params={'project_id': str(ObjectId())}
        )
        self.verify_test_result(result=result)
