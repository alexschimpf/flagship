from fastapi import APIRouter

from app.api.routes.feature_flags.routes import router as feature_flags_router

router = APIRouter()
router.include_router(feature_flags_router)
