import os

from rest_api_tester.runner import TestCaseRunner

from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestGetContextField(BaseTestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_get_context_field.json'
        self.runner = TestCaseRunner(
            client=test_client, path_to_scenarios_dir=path_to_scenarios_dir, default_content_type='application/json'
        )
        utils.clear_database()

    def test_get_context_field__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_context_field(project_id=project.project_id, context_field=utils.ContextField()) as context_field,
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_get_context_field__200',
                user=utils.User(),
                url_params={'project_id': project.project_id, 'context_field_id': context_field.context_field_id},
                response_json_modifiers={
                    'context_field_id': context_field.context_field_id,
                    'updated_date': context_field.updated_date.isoformat().replace('+00:00', 'Z'),
                    'created_date': context_field.created_date.isoformat().replace('+00:00', 'Z'),
                },
            )
            self.verify_test_result(result=result)
