import os
from rest_api_tester.runner import TestCaseRunner

from app.main import app
from tests.api.fastapi_test_client import FastAPITestClient
from tests.api.base_test_case import BaseTestCase
from tests.api import utils


class TestGetProjects(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_get_projects.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_get_projects__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_project(project=utils.Project(name='other'))
        ):
            project_id = project.project_id
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_get_projects__200',
                user=utils.User(projects=[project_id]),
                response_json_modifiers={
                    'items.[0].project_id': project_id,
                    'items.[0].created_date': project.created_date.isoformat(),
                    'items.[0].updated_date': project.updated_date.isoformat()
                }
            )
        self.verify_test_result(result=result)

