from typing import Any
from fastapi import APIRouter

from app.api.schemas import SuccessResponse
from app.services.database.mongodb import MongoDBService

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.get('/db/wipe', response_model=SuccessResponse)
def wipe_db() -> Any:
    # TODO: Protect (or remove) this route eventually
    MongoDBService.projects().drop()
    MongoDBService.users().drop()
    return SuccessResponse(success=True)
