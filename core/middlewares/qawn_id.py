import uuid

from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


request_id_contextvar = ContextVar("qawn_request_id", default=str(uuid.uuid4()))


def get_request_id():
    try:
        return request_id_contextvar.get()
    except Exception as e :
        return "NA"

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Qawn-Request-Id")
        request_id_contextvar.set(request_id)
        response = await call_next(request)
        return response




