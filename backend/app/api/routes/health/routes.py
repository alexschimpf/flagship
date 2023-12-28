from fastapi import APIRouter

router = APIRouter(
    prefix='/health',
    tags=['Health'],
    include_in_schema=False
)


@router.get('')
def get_health() -> str:
    return 'OK'
