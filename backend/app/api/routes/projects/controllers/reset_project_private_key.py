from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.projects.controllers import common
from app.api.routes.projects.schemas import ProjectWithPrivateKey
from app.services.database.mysql.models.project import ProjectModel
from app.services.database.mysql.service import MySQLService


class ResetProjectPrivateKeyController:

    def __init__(self, project_id: int):
        self.project_id = project_id

    def handle_request(self) -> ProjectWithPrivateKey:
        project_model, private_key = self._reset_private_key()
        if not project_model:
            raise NotFoundException

        return ProjectWithPrivateKey(
            project_id=project_model.project_id,
            name=project_model.name,
            private_key=private_key,
            created_date=project_model.created_date,
            updated_date=project_model.updated_date
        )

    def _reset_private_key(self) -> tuple[ProjectModel | None, str]:
        private_key, encrypted_private_key = common.generate_private_key()
        with MySQLService.get_session() as session:
            ProjectModel.update_project_private_key(
                project_id=self.project_id, private_key=encrypted_private_key, session=session)
            session.commit()

            project_model = session.get(ProjectModel, self.project_id)

        return project_model, private_key
