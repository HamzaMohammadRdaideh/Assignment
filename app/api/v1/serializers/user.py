import uuid
from typing import List
from pydantic import BaseModel, EmailStr

from app.api.v1.serializers.response import BaseResponse


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    uuid: str = uuid.uuid4()
    password: str


class UserResponse(BaseResponse):
    data: List[User]
