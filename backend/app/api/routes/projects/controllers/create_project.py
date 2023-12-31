from app.api.routes.projects.schemas import CreateOrUpdateProject, ProjectWithPrivateKey
from app.api.routes.projects.controllers import common
from app.services.database.mysql.service import MySQLService
from app.services.database.mysql.models.project import ProjectModel
from app.api.exceptions.exceptions import NameTakenException


class CreateProjectController:

    def __init__(self, request: CreateOrUpdateProject):
        self.request = request

    def handle_request(self) -> ProjectWithPrivateKey:
        self._validate()

        project_model, private_key = self._create_project()

        return ProjectWithPrivateKey(
            project_id=project_model.project_id,
            name=project_model.name,
            private_key=private_key,
            created_date=project_model.created_date,
            updated_date=project_model.updated_date
        )

    def _validate(self) -> None:
        with MySQLService.get_session() as session:
            if ProjectModel.get_project_by_name(name=self.request.name, session=session):
                raise NameTakenException(field='name')

    def _create_project(self) -> tuple[ProjectModel, str]:
        private_key, encrypted_private_key = common.generate_private_key()
        project_model = ProjectModel(
            name=self.request.name,
            private_key=encrypted_private_key
        )
        with MySQLService.get_session() as session:
            session.add(project_model)
            session.commit()
            session.refresh(project_model)

        return project_model, private_key
