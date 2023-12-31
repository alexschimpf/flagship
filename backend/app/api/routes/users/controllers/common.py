from sqlalchemy import select

from app.services.database.mysql.models.project import ProjectModel
from app.services.database.mysql.service import MySQLService


# TODO: Move to DB module
def are_projects_valid(project_ids: list[int]) -> bool:
    with MySQLService.get_session() as session:
        all_project_ids = set(
            session.scalars(
                select(
                    ProjectModel.project_id
                )
            ) or ()
        )

    for project_id in project_ids:
        if project_id not in all_project_ids:
            return False

    return True
