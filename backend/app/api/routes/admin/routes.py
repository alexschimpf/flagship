from fastapi import APIRouter, Depends

from app.api import auth
from app.api.routes.admin.controllers.get_audit_logs import GetAuditLogsController
from app.api.routes.admin.schemas import SystemAuditLogs
from app.api.schemas import User

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.get('/audit_logs', response_model=SystemAuditLogs)
def get_audit_logs(me: User = Depends(auth.get_user)) -> SystemAuditLogs:
    return GetAuditLogsController(
        me=me
    ).handle_request()
