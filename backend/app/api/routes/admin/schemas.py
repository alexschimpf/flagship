from datetime import datetime

from pydantic import BaseModel


class SystemAuditLog(BaseModel):
    actor: str
    event_time: datetime
    event_type: str
    details: str | None


class SystemAuditLogs(BaseModel):
    items: list[SystemAuditLog]
