from app.api.v1.views.health_check import router as beat_router
from app.api.v1.views.user import router as useer_router
from app.api.v1.views.candidate import router as profile_router
from app.api.v1.views.report import router as report_router

__all__ = (
    "useer_router",
    "profile_router",
    "report_router",
    "beat_router"
)
