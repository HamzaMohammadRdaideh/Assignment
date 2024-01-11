from fastapi import APIRouter
from app.api.v1.views import (useer_router, profile_router, report_router, beat_router)

api_router = APIRouter(prefix="/assignments/api/v1")
api_router.include_router(useer_router, tags=["User"])
api_router.include_router(profile_router, tags=["Profile"])
api_router.include_router(report_router, tags=["Report"])
api_router.include_router(beat_router, tags=["beat"])
