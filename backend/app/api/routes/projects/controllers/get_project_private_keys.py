from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.projects.schemas import ProjectPrivateKeys, ProjectPrivateKeyNameAndId
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.project_private_key import ProjectPrivateKeysTable
from app.services.database.mysql.service import MySQLService


class GetProjectPrivateKeysController:

    def __init__(self, project_id: int, me: User):
        self.project_id = project_id
        self.me = me

    def handle_request(self) -> ProjectPrivateKeys:
        if (not self.me.role.has_permission(Permission.READ_PROJECT_PRIVATE_KEYS) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            private_keys = ProjectPrivateKeysTable.get_project_private_keys(
                project_id=self.project_id, session=session)

        return ProjectPrivateKeys(items=[
            ProjectPrivateKeyNameAndId(
                project_private_key_id=private_key.project_private_key_id,
                name=private_key.name
            ) for private_key in private_keys
        ])
