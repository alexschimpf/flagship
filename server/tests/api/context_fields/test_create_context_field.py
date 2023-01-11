import os
import ujson
from typing import cast, Any, Callable
from rest_api_tester.runner import TestCaseRunner
from rest_api_tester.test import TestData

from app.main import app
from app.services.database.mongodb import types

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestCreateContextField(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_create_context_field__200(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_create_context_field.json',
                test_name='test_create_context_field__200',
                url_params={'project_id': str(project_id)}
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_create_context_field__200_enum_type(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_create_context_field.json',
                test_name='test_create_context_field__200_enum_type',
                url_params={'project_id': str(project_id)}
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_create_context_field__400_name_and_key_taken(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_context_field(
                project_id=project_id,
                name='tony',
                key='soprano',
                value_type=types.ContextValueType.STRING,
                description='ooooooo!'
            )
        ):
            result = self.runner.run(
                path_to_test_cases='test_create_context_field.json',
                test_name='test_create_context_field__400_name_and_key_taken',
                url_params={
                    'project_id': project_id
                }
            )
            self.verify_test_result(result=result)

    def test_create_context_field__400_missing_enum_def(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_create_context_field.json',
                test_name='test_create_context_field__400_missing_enum_def',
                url_params={
                    'project_id': project_id
                }
            )
            self.verify_test_result(result=result)

    def test_create_context_field__400_invalid_enum_def(self) -> None:
        def modifier(enum_def: dict[Any, Any]) -> Callable[[TestData], TestData]:
            def modifier_(test_data: TestData) -> TestData:
                request_data = ujson.loads(cast(str, test_data.request_data))
                request_data['enum_def'] = ujson.dumps(enum_def)
                test_data.request_data = ujson.dumps(request_data)
                return test_data

            return modifier_

        invalid_enum_defs: list[dict[Any, Any]] = [
            {'': 1},
            {' ': 1},
            {'a': ' '},
            {'a': [1]},
            {'a': {'b': 1}}
        ]
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            for invalid_enum_def in invalid_enum_defs:
                with self.subTest():
                    result = self.runner.run(
                        path_to_test_cases='test_create_context_field.json',
                        test_name='test_create_context_field__400_invalid_enum_def',
                        url_params={
                            'project_id': project_id
                        },
                        test_data_modifier=modifier(invalid_enum_def)
                    )
                    self.verify_test_result(result=result)
