from app.api.exceptions.exceptions import NameTakenException, UnauthorizedException
from app.api.routes.projects.controllers import common
from app.api.routes.projects.schemas import CreateOrUpdateProject, ProjectWithPrivateKey
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.project import ProjectRow, ProjectsTable
from app.services.database.mysql.service import MySQLService


class CreateProjectController:

    def __init__(self, request: CreateOrUpdateProject, me: User):
        self.request = request
        self.me = me

    def handle_request(self) -> ProjectWithPrivateKey:
        self._validate()

        project_row, private_key = self._create_project()

        return ProjectWithPrivateKey(
            project_id=project_row.project_id,
            name=project_row.name,
            private_key=private_key,
            created_date=project_row.created_date,
            updated_date=project_row.updated_date
        )

    def _validate(self) -> None:
        if not self.me.role.has_permission(Permission.CREATE_PROJECT):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            if ProjectsTable.get_project_by_name(name=self.request.name, session=session):
                raise NameTakenException(field='name')

    def _create_project(self) -> tuple[ProjectRow, str]:
        private_key, encrypted_private_key = common.generate_private_key()
        project_row = ProjectRow(
            name=self.request.name,
            private_key=encrypted_private_key
        )
        with MySQLService.get_session() as session:
            session.add(project_row)
            session.commit()
            session.refresh(project_row)

        return project_row, private_key
