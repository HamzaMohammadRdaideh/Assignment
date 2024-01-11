from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime, timezone
from typing import Union
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from app.api.v1.depandancies.hash import Hasher
from app.api.v1.serializers.user import User
from core.database.connection import db

SECRET_KEY = "skeleton"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/assignments/api/v1/users/login")


class TokenData(BaseModel):
    email: str


def get_user(email: str):
    user_collection = db.client["user"].users
    user = user_collection.find_one({"first_name": email})
    return user if user else False


def authenticate_user(email: str, password: str):
    email = email.lower()
    user = get_user(email=email)
    _pass = user.get("password")
    if not user:
        return False
    return user if Hasher().verify_password(password, _pass) else False


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
        token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise ValueError("Please provide a valid email")
        token_data = TokenData(email=email)
    except JWTError as e:
        raise e
    user = get_user(email=token_data.email)
    if user is None:
        raise ValueError("Invalid user")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise ValueError("Inactive user")
    return current_user
