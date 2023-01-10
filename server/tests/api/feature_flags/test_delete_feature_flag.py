import os
from bson import ObjectId
from rest_api_tester.runner import TestCaseRunner

from app.main import app

from tests.api import utils
from tests.api.client import FastAPITestClient
from tests.api.test import TestCase


class TestDeleteFeatureFlag(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        path_to_data = os.path.join(os.path.dirname(__file__), '__data__')
        client = FastAPITestClient(app=app)
        self.runner = TestCaseRunner(
            client=client,
            path_to_data=path_to_data,
            default_content_type='application/json'
        )

    def test_delete_feature_flag__200(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id,
            utils.new_feature_flag(
                project_id=project_id,
                name='tony',
                description='ooooooo!',
                enabled=True,
                conditions=[]
            ) as feature_flag_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_delete_feature_flag.json',
                test_name='test_delete_feature_flag__200',
                url_params={
                    'project_id': str(project_id),
                    'feature_flag_id': str(feature_flag_id)
                }
            )
            self.verify_test_result(result=result)

    def test_delete_feature_flag__404(self) -> None:
        with (
            utils.new_project(name='Waste Management, Inc.') as project_id
        ):
            result = self.runner.run(
                path_to_test_cases='test_delete_feature_flag.json',
                test_name='test_delete_feature_flag__404',
                url_params={
                    'project_id': str(project_id),
                    'feature_flag_id': str(ObjectId())
                }
            )
            self.verify_test_result(result=result)
