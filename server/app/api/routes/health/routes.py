from fastapi import APIRouter

health_router = APIRouter(
    prefix='/health',
    tags=['health'],
    include_in_schema=False
)


@health_router.get('')
def get_health() -> str:
    return 'OK'


@health_router.get('/deps')
def get_deps() -> str:
    return 'OK'
