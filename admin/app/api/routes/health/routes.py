from fastapi import APIRouter

router = APIRouter(prefix='/health', tags=['Health'], include_in_schema=False)


@router.get('')
def get_health() -> str:
    return 'Ok'


@router.get('/deps')
def get_deps() -> str:
    return 'Ok'
