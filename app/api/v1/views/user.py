import json
from datetime import timedelta

from bson import json_util
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette import status

from app.api.v1.depandancies.authorization import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_user,
    SECRET_KEY,
    ALGORITHM,
)
from app.api.v1.repositories import user
from app.api.v1.serializers.user import UserResponse, User
from core.constans.response_messages import ResponseConstants
from core.middlewares.catch_exceptions import logger
from utils.http_response import http_response

router = APIRouter(prefix="/users")


@router.get("/", response_model=UserResponse)
def list_user():
    """
    Retrieve a list of users.
    """
    data = user.list_users()
    return http_response(
        data=data, message=ResponseConstants.CREATED_MSG, status=status.HTTP_200_OK
    )


@router.post("/", response_model=UserResponse)
def create_user(request_body: User):
    """
    Create a new user.
    """
    logger.info(f"Request Body: {request_body}")
    data = user.create_user(request_body)
    return http_response(
        data=dict(data), message=ResponseConstants.CREATED_MSG, status=status.HTTP_201_CREATED
    )


@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get access token for user login.
    """
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise ValueError(f"Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_token(token: str):
    """
    Get user token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print("username extracted is ", email)
        if email is None:
            raise ValueError(f"Incorrect email")
    except JWTError as e:
        raise e
    user = get_user(email=email)
    if user is None:
        raise ValueError("Invalid user")
    user = json.loads(json_util.dumps(user))
    return jsonable_encoder(user)


@router.get("/me")
async def get_current_user_from_token(token: str):
    """
    Get current user from token.
    """
    return get_token(token)
