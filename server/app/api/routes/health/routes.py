from fastapi import APIRouter

router = APIRouter(
    prefix='/health',
    tags=['health'],
    include_in_schema=False
)


@router.get('')
def get_health() -> str:
    return 'OK'


@router.get('/deps')
def get_deps() -> str:
    return 'OK'
