import os
import ujson
from typing import Any, Callable, cast
from rest_api_tester.runner import TestCaseRunner
from rest_api_tester.test import TestData

from app.main import app
from app.services.database.mongodb.types import FeatureFlagCondition, Operator, ContextValueType

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test_case import TestCase


class TestCreateFeatureFlag(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_create_feature_flag__200(self) -> None:
        with utils.new_project(name='Waste Management, Inc.') as project_id:
            result = self.runner.run(
                path_to_test_cases='test_create_feature_flag.json',
                test_name='test_create_feature_flag__200',
                url_params={'project_id': str(project_id)}
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_create_feature_flag__400_name_taken(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_feature_flag(
                project_id=project_id,
                name='tony',
                description='ooooooo!',
                enabled=False,
                conditions=[]
            )
        ):
            result = self.runner.run(
                path_to_test_cases='test_create_feature_flag.json',
                test_name='test_create_feature_flag__400_name_taken',
                url_params={'project_id': str(project_id)}
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_create_feature_flag__400_invalid_conditions(self) -> None:
        def modifier(conditions: Any) -> Callable[[TestData], TestData]:
            def modifier_(test_data: TestData) -> TestData:
                request_data = ujson.loads(cast(str, test_data.request_data))
                request_data['conditions'] = conditions
                test_data.request_data = ujson.dumps(request_data)
                return test_data

            return modifier_

        invalid_conditions_tests: Any = [
            [[FeatureFlagCondition(context_key='string', value=[], operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='string', value={}, operator=Operator.NOT_EQUALS)]],
            [[FeatureFlagCondition(context_key='string', value=None, operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='string', value='abc', operator=Operator.GREATER_THAN)]],
            [[FeatureFlagCondition(context_key='string', value=[[]], operator=Operator.IN_LIST)]],

            [[FeatureFlagCondition(context_key='integer', value='x', operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='integer', value='4.2', operator=Operator.GREATER_THAN)]],
            [[FeatureFlagCondition(context_key='integer', value=4.2, operator=Operator.LESS_THAN)]],
            [[FeatureFlagCondition(context_key='integer', value='', operator=Operator.NOT_EQUALS)]],
            [[FeatureFlagCondition(context_key='integer', value=1, operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='integer', value=['x'], operator=Operator.IN_LIST)]],

            [[FeatureFlagCondition(context_key='number', value='x', operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='number', value='4.2x', operator=Operator.GREATER_THAN)]],
            [[FeatureFlagCondition(context_key='number', value='', operator=Operator.NOT_EQUALS)]],
            [[FeatureFlagCondition(context_key='number', value=1, operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='number', value=1.2, operator=Operator.NOT_INTERSECTS)]],
            [[FeatureFlagCondition(context_key='number', value=['x'], operator=Operator.IN_LIST)]],

            [[FeatureFlagCondition(context_key='boolean', value='yes', operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='boolean', value='no', operator=Operator.NOT_EQUALS)]],
            [[FeatureFlagCondition(context_key='boolean', value=1, operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='boolean', value='1', operator=Operator.NOT_EQUALS)]],
            [[FeatureFlagCondition(context_key='boolean', value='', operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='boolean', value='true', operator=Operator.GREATER_THAN)]],
            [[FeatureFlagCondition(context_key='boolean', value=False, operator=Operator.LESS_THAN)]],
            [[FeatureFlagCondition(context_key='integer', value=['yes'], operator=Operator.IN_LIST)]],

            [[FeatureFlagCondition(context_key='version', value=[], operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='version', value={}, operator=Operator.NOT_EQUALS)]],
            [[FeatureFlagCondition(context_key='version', value=None, operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='version', value='1.2.3', operator=Operator.NOT_CONTAINS)]],

            [[FeatureFlagCondition(context_key='enum', value=[], operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='enum', value={}, operator=Operator.NOT_EQUALS)]],
            [[FeatureFlagCondition(context_key='enum', value=None, operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='enum', value=[1], operator=Operator.EQUALS)]],
            [[FeatureFlagCondition(context_key='enum', value=[[]], operator=Operator.IN_LIST)]],

            [[FeatureFlagCondition(context_key='string_list', value=[], operator=Operator.CONTAINS)]],
            [[FeatureFlagCondition(context_key='string_list', value={}, operator=Operator.NOT_CONTAINS)]],
            [[FeatureFlagCondition(context_key='string_list', value=None, operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='string_list', value=[['1']], operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='string_list', value=[True], operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='string_list', value=['1'], operator=Operator.EQUALS)]],

            [[FeatureFlagCondition(context_key='integer_list', value=[], operator=Operator.CONTAINS)]],
            [[FeatureFlagCondition(context_key='integer_list', value={}, operator=Operator.NOT_CONTAINS)]],
            [[FeatureFlagCondition(context_key='integer_list', value=None, operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='integer_list', value=[['1']], operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='integer_list', value=[True], operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='integer_list', value=[1], operator=Operator.EQUALS)]],

            [[FeatureFlagCondition(context_key='enum_list', value=[], operator=Operator.CONTAINS)]],
            [[FeatureFlagCondition(context_key='enum_list', value={}, operator=Operator.NOT_CONTAINS)]],
            [[FeatureFlagCondition(context_key='enum_list', value=None, operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='enum_list', value=[['1']], operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='enum_list', value=[True], operator=Operator.INTERSECTS)]],
            [[FeatureFlagCondition(context_key='enum_list', value=[1], operator=Operator.EQUALS)]]
        ]
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_context_field(
                project_id=project_id,
                name='integer',
                key='integer',
                value_type=ContextValueType.INTEGER,
                description=''
            ),
            utils.new_context_field(
                project_id=project_id,
                name='string',
                key='string',
                value_type=ContextValueType.STRING,
                description=''
            ),
            utils.new_context_field(
                project_id=project_id,
                name='number',
                key='number',
                value_type=ContextValueType.NUMBER,
                description=''
            ),
            utils.new_context_field(
                project_id=project_id,
                name='boolean',
                key='boolean',
                value_type=ContextValueType.BOOLEAN,
                description=''
            ),
            utils.new_context_field(
                project_id=project_id,
                name='version',
                key='version',
                value_type=ContextValueType.VERSION,
                description=''
            ),
            utils.new_context_field(
                project_id=project_id,
                name='enum',
                key='enum',
                value_type=ContextValueType.ENUM,
                description='',
                enum_def=ujson.dumps({'test': 1})
            ),
            utils.new_context_field(
                project_id=project_id,
                name='enum_list',
                key='enum_list',
                value_type=ContextValueType.ENUM_LIST,
                description='',
                enum_def=ujson.dumps({'test': 1})
            ),
            utils.new_context_field(
                project_id=project_id,
                name='string_list',
                key='string_list',
                value_type=ContextValueType.STRING_LIST,
                description=''
            ),
            utils.new_context_field(
                project_id=project_id,
                name='integer_list',
                key='integer_list',
                value_type=ContextValueType.INTEGER_LIST,
                description=''
            )
        ):
            for invalid_conditions in invalid_conditions_tests:
                with self.subTest():
                    result = self.runner.run(
                        path_to_test_cases='test_create_feature_flag.json',
                        test_name='test_create_feature_flag__400_invalid_conditions',
                        url_params={'project_id': str(project_id)},
                        test_data_modifier=modifier(invalid_conditions)
                    )
                    self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
                    try:
                        self.verify_test_result(result=result)
                    except Exception:
                        print(f'\nFailed case: {ujson.dumps(invalid_conditions)}\n')  # noqa
                        raise
