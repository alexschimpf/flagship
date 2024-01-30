import os

from rest_api_tester.runner import TestCaseRunner

from app.api.routes.feature_flags.schemas import FeatureFlagCondition
from app.constants import Operator
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
            default_content_type='application/json',
        )
        utils.clear_database()

    def test_get_audit_logs__200(self) -> None:
        with (
            utils.new_project(project=utils.Project()) as project,
            utils.new_feature_flag(
                project_id=project.project_id, feature_flag=utils.FeatureFlag()) as feature_flag,
            utils.new_feature_flag_audit_log(
                project_id=project.project_id, feature_flag_id=feature_flag.feature_flag_id,
                audit_log=utils.FeatureFlagAuditLog()
            ) as audit_log_1,
            utils.new_feature_flag_audit_log(
                project_id=project.project_id, feature_flag_id=feature_flag.feature_flag_id,
                audit_log=utils.FeatureFlagAuditLog(description='New description')
            ) as audit_log_2,
            utils.new_feature_flag_audit_log(
                project_id=project.project_id, feature_flag_id=feature_flag.feature_flag_id,
                audit_log=utils.FeatureFlagAuditLog(
                    actor='other@email.com', name='New name', enabled=False, description='Newest description',
                    conditions=[[FeatureFlagCondition(context_key='context_key', operator=Operator.EQUALS, value='1')]])
            ) as audit_log_3
        ):
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_get_audit_logs__200',
                user=utils.User(),
                url_params={
                    'feature_flag_id': feature_flag.feature_flag_id,
                    'project_id': project.project_id
                },
                response_json_modifiers={
                    'items.[0].event_time': audit_log_1.created_date.isoformat().replace('+00:00', 'Z'),
                    'items.[1].event_time': audit_log_2.created_date.isoformat().replace('+00:00', 'Z'),
                    'items.[2].event_time': audit_log_3.created_date.isoformat().replace('+00:00', 'Z')
                }
            )
            self.verify_test_result(result=result)
