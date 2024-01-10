from datetime import datetime

from pydantic import BaseModel, EmailStr


class SystemAuditLog(BaseModel):
    actor: EmailStr
    event_time: datetime
    event_type: str
    details: str | None


class SystemAuditLogs(BaseModel):
    items: list[SystemAuditLog]
