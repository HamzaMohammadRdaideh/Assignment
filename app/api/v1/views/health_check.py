from fastapi import APIRouter, status
from utils.http_response import http_response

from core.constans.response_messages import ResponseConstants

router = APIRouter()


@router.get('/beat')
def health_check():
    return http_response(data=[], status=status.HTTP_200_OK,
                         message=ResponseConstants.RETRIEVED_MSG)
