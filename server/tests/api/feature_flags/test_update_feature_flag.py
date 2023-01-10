import os
from bson import ObjectId
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from app.services.database.mongodb import types

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test import TestCase


class TestUpdateFeatureFlag(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_update_feature_flag__200(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_feature_flag(
                project_id=project_id,
                name='tony?',
                description='ooooooo!?',
                enabled=False,
                conditions=[[types.FeatureFlagCondition(
                    context_key='tony?',
                    operator=types.Operator.NOT_CONTAINS,
                    value='soprano?'
                )]]
            ) as feature_flag_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_update_feature_flag.json',
                test_name='test_update_feature_flag__200',
                url_params={
                    'project_id': str(project_id),
                    'feature_flag_id': str(feature_flag_id)
                }
            )
            self.ignore_expected_response_fields(result=result, fields=self.DEFAULT_IGNORE_FIELDS)
            self.verify_test_result(result=result)

    def test_update_feature_flag__404(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_update_feature_flag.json',
                test_name='test_update_feature_flag__404',
                url_params={
                    'project_id': str(project_id),
                    'feature_flag_id': str(ObjectId())
                }
            )
            self.verify_test_result(result=result)

    def test_update_feature_flag__400_name_taken(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_feature_flag(
                project_id=project_id,
                name='tony',
                description='ooooooo!',
                enabled=False,
                conditions=[]
            ),
            utils.new_feature_flag(
                project_id=project_id,
                name='tony?',
                description='ooooooo!?',
                enabled=False,
                conditions=[]
            ) as feature_flag_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_update_feature_flag.json',
                test_name='test_update_feature_flag__400_name_taken',
                url_params={
                    'project_id': str(project_id),
                    'feature_flag_id': str(feature_flag_id)
                }
            )
            self.verify_test_result(result=result)
