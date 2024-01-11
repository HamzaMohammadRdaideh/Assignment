from bson import ObjectId
from fastapi import APIRouter, Depends, status

from app.api.v1.repositories import candidate
from app.api.v1.serializers.candidate import CandidateResponse, Candidate
from app.api.v1.views.user import get_current_user_from_token
from core.constans.response_messages import ResponseConstants
from core.middlewares.catch_exceptions import logger
from utils.http_response import http_response

router = APIRouter(prefix="/profile")


@router.post("/", response_model=CandidateResponse)
def create_candidate(request_body: Candidate):
    """
    Create a new candidate profile.
    """
    logger.info(f"Request Body: {request_body}")
    data = candidate.create_candidate(request_body)

    if isinstance(data.get('_id'), ObjectId):
        data['_id'] = str(data['_id'])

    return http_response(
        data=data, message=ResponseConstants.CREATED_MSG, status=status.HTTP_201_CREATED
    )


@router.get("/", response_model=CandidateResponse)
def list_candidates(current_user: str = Depends(get_current_user_from_token)):
    """
    Get a list of all candidates.
    """
    data = candidate.get_all_candidates()
    return http_response(
        data=data, message=ResponseConstants.RETRIEVED, status=status.HTTP_200_OK
    )


@router.get("/profile", response_model=CandidateResponse)
def specific_candidate(uuid: str = None, current_user: str = Depends(get_current_user_from_token)):
    """
    Get a specific candidate profile by UUID.
    """
    data = candidate.specific_candidate(uuid)
    return http_response(
        data=data, message=ResponseConstants.RETRIEVED, status=status.HTTP_200_OK
    )


@router.delete("/")
def specific_profile(uuid: str):
    """
    Delete a specific candidate profile by UUID.
    """
    data = candidate.delete_specific_candidate(uuid)
    return http_response(
        data=data, message=ResponseConstants.DELETED, status=status.HTTP_200_OK
    )


@router.patch("/")
def patch_specific_profile(uuid: str, request_body: Candidate):
    """
    Update a specific candidate profile by UUID.
    """
    data = candidate.patch_specific_profile(uuid, request_body)
    return http_response(
        data=data, message=ResponseConstants.DELETED, status=status.HTTP_200_OK
    )