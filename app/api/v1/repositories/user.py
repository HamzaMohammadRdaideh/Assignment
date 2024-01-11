from fastapi.encoders import jsonable_encoder

from app.api.v1.depandancies.hash import Hasher
from core.database.connection import db
from core.exceptions.user import UserCreateError


def list_users():
    user_collection = db.client["user"].users
    data = []
    for record in user_collection.find():
        record["_id"] = str(record["_id"])
        data.append(record)

    response = jsonable_encoder(data)
    return response


def create_user(request_body):
    request_body.password = Hasher().get_password_hash(request_body.password)
    try:
        user_collection = db.client["user"].users
        user_collection.insert_one(request_body.dict())
        return request_body
    except Exception as e:
        raise UserCreateError
