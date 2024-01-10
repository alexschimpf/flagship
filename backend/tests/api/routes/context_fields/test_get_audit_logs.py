import os

from rest_api_tester.runner import TestCaseRunner

from app.main import app
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestGetAuditLogs(BaseTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_get_audit_logs.json'
        self.runner = TestCaseRunner(
            client=test_client,
            path_to_scenarios_dir=path_to_scenarios_dir,
            default_content_type='application/json'
        )
        utils.clear_database()

    def test_get_audit_logs__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_context_field(
                project_id=project.project_id, context_field=utils.ContextField()) as context_field,
            utils.new_context_field_audit_log(
                project_id=project.project_id, context_field_id=context_field.context_field_id,
                audit_log=utils.ContextFieldAuditLog()
            ) as audit_log_1,
            utils.new_context_field_audit_log(
                project_id=project.project_id, context_field_id=context_field.context_field_id,
                audit_log=utils.ContextFieldAuditLog(description='New description')
            ) as audit_log_2,
            utils.new_context_field_audit_log(
                project_id=project.project_id, context_field_id=context_field.context_field_id,
                audit_log=utils.ContextFieldAuditLog(
                    actor='other@email.com', name='New name', enum_def={'a': 1, 'b': 2})
            ) as audit_log_3
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_get_audit_logs__200',
                user=utils.User(),
                url_params={
                    'context_field_id': context_field.context_field_id,
                    'project_id': project.project_id
                },
                response_json_modifiers={
                    'items.[0].event_time': audit_log_1.created_date.isoformat(),
                    'items.[1].event_time': audit_log_2.created_date.isoformat(),
                    'items.[2].event_time': audit_log_3.created_date.isoformat()
                }
            )
            self.verify_test_result(result=result)
