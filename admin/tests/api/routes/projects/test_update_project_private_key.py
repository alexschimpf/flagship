import os

from rest_api_tester.runner import TestCaseRunner
from sqlalchemy import select

from app.constants import UserRole
from app.main import app
from app.services.database.mysql.schemas.project_private_key import ProjectPrivateKeyRow
from app.services.database.mysql.service import MySQLService
from tests.api import utils
from tests.api.base_test_case import BaseTestCase
from tests.api.fastapi_test_client import FastAPITestClient


class TestUpdateProjectPrivateKey(BaseTestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        test_client = FastAPITestClient(app=app)
        path_to_scenarios_dir = os.path.join(os.path.dirname(__file__), '__scenarios__')
        self.path_to_test_cases = 'test_update_project_private_key.json'
        self.runner = TestCaseRunner(
            client=test_client, path_to_scenarios_dir=path_to_scenarios_dir, default_content_type='application/json'
        )
        utils.clear_database()

    def test_update_project_private_key__200(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            with MySQLService.get_session() as session:
                project_private_key_id = session.scalar(
                    select(ProjectPrivateKeyRow.project_private_key_id)
                    .where(ProjectPrivateKeyRow.project_id == project.project_id)
                    .limit(1)
                )

            project_id = project.project_id
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_project_private_key__200',
                user=utils.User(projects=[project_id]),
                url_params={'project_id': project_id, 'project_private_key_id': project_private_key_id},
            )
            self.verify_test_result(result=result)

    def test_update_project_private_key__403_read_only_role(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            with MySQLService.get_session() as session:
                project_private_key_id = session.scalar(
                    select(ProjectPrivateKeyRow.project_private_key_id)
                    .where(ProjectPrivateKeyRow.project_id == project.project_id)
                    .limit(1)
                )

            project_id = project.project_id
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_project_private_key__403_read_only_role',
                user=utils.User(projects=[project_id], role=UserRole.READ_ONLY),
                url_params={'project_id': project_id, 'project_private_key_id': project_private_key_id},
            )
            self.verify_test_result(result=result)

    def test_update_project_private_key__403_project_not_assigned_to_user(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            with MySQLService.get_session() as session:
                project_private_key_id = session.scalar(
                    select(ProjectPrivateKeyRow.project_private_key_id)
                    .where(ProjectPrivateKeyRow.project_id == project.project_id)
                    .limit(1)
                )

            project_id = project.project_id
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_project_private_key__403_project_not_assigned_to_user',
                user=utils.User(),
                url_params={'project_id': project_id, 'project_private_key_id': project_private_key_id},
            )
            self.verify_test_result(result=result)

    def test_update_project_private_key__404(self) -> None:
        with utils.new_project(project=utils.Project()) as project:
            project_id = project.project_id
            result = self.run_test_with_user(
                runner=self.runner,
                path_to_test_cases=self.path_to_test_cases,
                test_name='test_update_project_private_key__404',
                user=utils.User(projects=[project_id]),
                url_params={'project_id': project_id},
            )
            self.verify_test_result(result=result)
