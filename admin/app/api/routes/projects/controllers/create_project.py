from app.api.exceptions.exceptions import NameTakenException, UnauthorizedException
from app.api.routes.projects.controllers import common
from app.api.routes.projects.schemas import CreateOrUpdateProject, ProjectWithPrivateKey
from app.api.schemas import User
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.project import ProjectRow, ProjectsTable
from app.services.database.mysql.schemas.project_private_key import ProjectPrivateKeyRow
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.schemas.user_project import UserProjectRow
from app.services.database.mysql.service import MySQLService
from app.services.database.redis.service import RedisService


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
            updated_date=project_row.updated_date,
        )

    def _validate(self) -> None:
        if not self.me.role.has_permission(Permission.CREATE_PROJECT):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            if ProjectsTable.get_project_by_name(name=self.request.name, session=session):
                raise NameTakenException(field='name')

    def _create_project(self) -> tuple[ProjectRow, str]:
        with MySQLService.get_session() as session:
            private_key, encrypted_private_key = common.generate_private_key()
            project_row = ProjectRow(name=self.request.name)

            session.add(project_row)
            session.flush()

            session.add(UserProjectRow(user_id=self.me.user_id, project_id=project_row.project_id))
            session.add(
                ProjectPrivateKeyRow(
                    project_id=project_row.project_id, private_key=encrypted_private_key, name='First private key'
                )
            )
            session.add(
                SystemAuditLogRow(
                    actor=self.me.email,
                    event_type=AuditLogEventType.CREATED_PROJECT,
                    details=f'Name: {project_row.name}',
                )
            )

            session.commit()
            session.refresh(project_row)

        RedisService.add_project_private_key(
            project_id=project_row.project_id, encrypted_private_key=encrypted_private_key
        )

        return project_row, private_key
