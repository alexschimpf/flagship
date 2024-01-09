from typing import cast

from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.routes.projects.controllers import common
from app.api.routes.projects.schemas import PrivateKey
from app.api.schemas import User
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.project import ProjectRow
from app.services.database.mysql.schemas.project_private_key import ProjectPrivateKeyRow
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.service import MySQLService


class CreateProjectPrivateKeyController:

    def __init__(self, project_id: int, me: User):
        self.project_id = project_id
        self.me = me

    def handle_request(self) -> PrivateKey:
        name = self._validate()
        project_row, private_key = self._create_private_key(name=name)

        return PrivateKey(
            private_key=private_key
        )

    def _validate(self) -> str:
        if (not self.me.role.has_permission(Permission.CREATE_PROJECT_PRIVATE_KEY) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            row = session.get(ProjectRow, self.project_id)
            if not row:
                raise NotFoundException

        return row.name

    def _create_private_key(self, name: str) -> tuple[ProjectRow, str]:
        private_key, encrypted_private_key = common.generate_private_key()
        with MySQLService.get_session() as session:
            session.add(ProjectPrivateKeyRow(
                project_id=self.project_id,
                private_key=encrypted_private_key
            ))
            session.add(SystemAuditLogRow(
                actor=self.me.email,
                event_type=AuditLogEventType.ADDED_PROJECT_PRIVATE_KEY,
                details=f'Name: {name}'
            ))
            session.commit()

            project_row = session.get(ProjectRow, self.project_id)

        return cast(ProjectRow, project_row), private_key
