from app.api.exceptions.exceptions import UnauthorizedException, NotFoundException
from app.api.routes.projects.schemas import ProjectPrivateKeyName
from app.api.schemas import User, SuccessResponse
from app.constants import Permission
from app.services.database.mysql.schemas.project_private_key import ProjectPrivateKeysTable, ProjectPrivateKeyRow
from app.services.database.mysql.service import MySQLService


class UpdateProjectPrivateKeyController:

    def __init__(self, project_id: int, project_private_key_id: int, request: ProjectPrivateKeyName, me: User):
        self.project_id = project_id
        self.project_private_key_id = project_private_key_id
        self.request = request
        self.me = me

    def handle_request(self) -> SuccessResponse:
        if (not self.me.role.has_permission(Permission.READ_PROJECT_PRIVATE_KEYS) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            if not session.get(ProjectPrivateKeyRow, (self.project_private_key_id, self.project_id)):
                raise NotFoundException

            ProjectPrivateKeysTable.update_project_private_keys(
                project_id=self.project_id, project_private_key_id=self.project_private_key_id,
                name=self.request.name, session=session
            )
            session.commit()

        return SuccessResponse()
