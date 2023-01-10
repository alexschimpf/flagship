import os
from rest_api_tester.runner import TestCaseRunner

from app.main import app

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test import TestCase


class TestContextFields(TestCase):

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

    def test_get_context_field__200(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_context_field(
                project_id=project_id,
                name='tony',
                key='soprano',
                value_type='string',
                description='ooooooo!'
            ) as context_field_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_get_context_field.json',
                test_name='test_get_context_field__200',
                url_params={
                    'project_id': str(project_id),
                    'context_field_id': str(context_field_id)
                }
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_get_context_fields__200(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_context_field(
                project_id=project_id,
                name='tony',
                key='soprano',
                value_type='string',
                description='ooooooo!'
            )
        ):
            result = self.runner.run(
                path_to_test_cases='test_get_context_fields.json',
                test_name='test_get_context_fields__200',
                url_params={'project_id': str(project_id)}
            )
            actual_items = result.response.json()['items']
            self.replace_response_strings(
                result=result,
                id=actual_items[0]['_id'],
                created_date=actual_items[0]['created_date'],
                updated_date=actual_items[0]['updated_date']
            )
            self.verify_test_result(result=result)

    def test_create_context_field__200(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_create_context_field.json',
                test_name='test_create_context_field__200',
                url_params={'project_id': str(project_id)}
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_update_context_field__200(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_context_field(
                project_id=project_id,
                name='tony?',
                key='soprano?',
                value_type='string?',
                description='ooooooo!?'
            ) as context_field_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_update_context_field.json',
                test_name='test_update_context_field__200',
                url_params={
                    'project_id': str(project_id),
                    'context_field_id': str(context_field_id)
                }
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_delete_context_field__200(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_context_field(
                project_id=project_id,
                name='tony?',
                key='soprano?',
                value_type='string?',
                description='ooooooo!?'
            ) as context_field_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_delete_context_field.json',
                test_name='test_delete_context_field__200',
                url_params={
                    'project_id': str(project_id),
                    'context_field_id': str(context_field_id)
                }
            )
            self.verify_test_result(result=result)
