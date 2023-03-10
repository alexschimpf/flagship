import os
from bson import ObjectId
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from app.services.database.mongodb import types

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestGetContextField(TestCase):

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
                value_type=types.ContextValueType.STRING,
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

    def test_get_context_field__404(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_get_context_field.json',
                test_name='test_get_context_field__404',
                url_params={
                    'project_id': str(project_id),
                    'context_field_id': str(ObjectId())
                }
            )
            self.verify_test_result(result=result)
