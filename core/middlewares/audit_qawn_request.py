from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from core.middlewares.catch_exceptions import logger
from core.middlewares.qawn_id import get_request_id
from datetime import datetime
from integrations.aws_queue.aws_sqs import send_message_to_sqs
from core.settings.base import env_settings
import json

AUDIT_QUEUE_URL = env_settings.AUDIT_QUEUE_URL


class AuditQawnRequestMiddleware(BaseHTTPMiddleware):
    async def get_response(self, request: Request, call_next):
        try:
            response = await call_next(request)

            response_status_code = response.status_code
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            response_payload = json.loads(response_body.decode("utf-8"))
            if "message" in response_payload:
                response_body = response_payload.get("message")

        except Exception as exc:
            if len(exc.args) == 2:
                response_status_code = exc.args[0]
                response_body = exc.args[1]
            else:
                response_status_code = str(500)
                response_body = str(exc)
        return response_body, response_status_code

    async def dispatch(self, request: Request, call_next):
        response_body, response_status_code = await self.get_response(
            request, call_next
        )

        auth_token = request.headers.get("Authorization")
        if auth_token:
            request_body = ""
            if request.method in {"POST", "PATCH"} and "/image" in request.url.path:
                content_type = request.headers.get("content-type", "")
                if "multipart/form-data" in content_type:
                    request_body = ""
                else:
                    request_body = str(request.body())
            elif request.method in {"GET", "DELETE"}:
                request_body = ""
            else:
                request_body = request_body

            request_id = get_request_id()
            ip_address = str(request.headers.get("ip-address", ""))
            geolocation = str(request.headers.get("geolocation", ""))
            qawn_release = str(request.headers.get("qawn-release"))
            os_version = str(request.headers.get("os-version"))
            device_os = str(request.headers.get("device-os"))
            login_method = str(request.headers.get("login-method", ""))
            qawn_device_id = request.headers.get("qawn-device-id", "")

            data = {
                "payload": {
                    "request_path": str(request.url.path),
                    "request_headers": {
                        "authorization": auth_token,
                        "qawn_device_id": qawn_device_id,
                        "ip_address": ip_address,
                        "geolocation": geolocation,
                        "qawn_release": qawn_release,
                        "os_version": os_version,
                        "device_os": device_os,
                        "login_method": login_method,
                    },
                    "request_body": request_body,
                    "request_time": str(datetime.now()),
                    "service_name": "ekyc",
                    "response_body": response_body,
                    "status_code": response_status_code,
                },
                "function": "audit_qawn_user_request",
            }

            try:
                msg_attributes = {
                    "X-Qawn-Request-Id": {
                        "DataType": "String",
                        "StringValue": str(request_id),
                    }
                }
                send_message_to_sqs(
                    message=json.dumps(data),
                    msg_attributes=msg_attributes,
                    queue_url=AUDIT_QUEUE_URL,
                )
                logger.info(
                    f"## Message Pushed Successfully to the Audit Queue with payload ==> {data}"
                )
            except Exception as exc:
                logger.critical(
                    f"## Failed to Push Message to the Queue with exception ==> {str(exc)}##"
                )
