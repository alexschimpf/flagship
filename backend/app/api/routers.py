from fastapi import APIRouter

from app.api.routes.auth.routes import router as auth_router
from app.api.routes.context_fields.routes import router as context_fields_router
from app.api.routes.feature_flags.routes import router as feature_flags_router
from app.api.routes.health.routes import router as health_router
from app.api.routes.projects.routes import router as projects_router
from app.api.routes.users.routes import router as users_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(projects_router)
router.include_router(feature_flags_router)
router.include_router(context_fields_router)
router.include_router(health_router)
