from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.api.v1.repositories import report

router = APIRouter()


@router.get("/generate-report", response_class=StreamingResponse)
def generate_report_endpoint():
    return report.generate_report()
