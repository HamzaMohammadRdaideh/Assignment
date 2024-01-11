import logging.config
import time
import traceback

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from utils.http_response import http_response

logging.config.fileConfig("logging.conf", disable_existing_loggers=True)

logger = logging.getLogger(__name__)


class ExceptionMiddleWare(BaseHTTPMiddleware):
    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def log_requests(self, request, call_next):
        if (
            "beat" not in request.url.path
            and "/docs" not in request.url.path
            and "/openapi.json" not in request.url.path
        ):
            logger.info(
                f" Request: {request.method} {request.url.path} {request.url.query}"
            )

            # Todo exclude files in the body from address, financial and fatca

            start_time = time.time()
            response = await call_next(request)

            process_time = (time.time() - start_time) * 1000
            formatted_process_time = "{0:.2f}".format(process_time)
            logger.info(
                f" Response: {response.status_code} in {formatted_process_time}ms"
            )

        else:
            return await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        if "beat" not in request.url.path:
            logger.info(response_body)
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    async def dispatch(self, request: Request, call_next):
        try:
            response = await self.log_requests(request, call_next)
            return response
        except Exception as e:
            logger.info(
                f"request: {request.method} {request.url.path} {request.url.query}"
            )

            # Todo exclude files in the body from address, financial and fatca

            start_time = time.time()
            process_time = (time.time() - start_time) * 1000
            formatted_process_time = "{0:.2f}".format(process_time)

            traceback_object = traceback.format_exc(limit=None, chain=True).split(
                "File"
            )[-1]

            if len(e.args) == 2:
                message = e.args[0]
                status = e.args[1]
                logger.exception(
                    f" Response: {status} in {formatted_process_time}ms, message: {message} , description : {traceback_object}"
                )

            else:
                message = str(e)
                status = 500
                logger.critical(
                    f" Response: {status} in {formatted_process_time}ms, message: {message} , description : {traceback_object}"
                )
            return http_response(status=status, message=message)
