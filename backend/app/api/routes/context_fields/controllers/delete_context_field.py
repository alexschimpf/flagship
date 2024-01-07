from sqlalchemy.orm import Session

from app.api.exceptions.exceptions import NotFoundException, ContextFieldInUseException, UnauthorizedException
from app.api.schemas import SuccessResponse, User
from app.constants import Permission
from app.services.database.mysql.schemas.context_field import ContextFieldsTable, ContextFieldRow
from app.services.database.mysql.schemas.feature_flag import FeatureFlagsTable
from app.services.database.mysql.service import MySQLService


class DeleteContextFieldController:

    def __init__(self, project_id: int, context_field_id: int, me: User):
        self.project_id = project_id
        self.context_field_id = context_field_id
        self.me = me

    def handle_request(self) -> SuccessResponse:
        self._validate()
        self._delete_context_field()

        return SuccessResponse()

    def _validate(self) -> None:
        if (not self.me.role.has_permission(Permission.DELETE_CONTEXT_FIELD) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            context_field_row = session.get(ContextFieldRow, (self.context_field_id, self.project_id))
            if not context_field_row:
                raise NotFoundException

            if self.is_context_field_key_used(field_key=context_field_row.field_key, session=session):
                raise ContextFieldInUseException

    def is_context_field_key_used(self, field_key: str, session: Session) -> bool:
        feature_flags = FeatureFlagsTable.get_feature_flags(project_id=self.project_id, session=session)
        for feature_flag in feature_flags:
            if f'"context_key":"{field_key}"' in feature_flag.conditions:
                return True

        return False

    def _delete_context_field(self) -> None:
        with MySQLService.get_session() as session:
            ContextFieldsTable.delete_context_field(
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                session=session
            )
            session.commit()
