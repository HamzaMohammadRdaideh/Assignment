import logging
from types import FrameType
from typing import cast

from loguru import logger
from pythonjsonlogger.jsonlogger import JsonFormatter

from core.middlewares import get_request_id


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class CustomJsonFormatter(JsonFormatter):
    """
    this class defines the json format that will be displayed for logging records
    """
    def add_fields(self, log_record, record, message_dict):
        log_record["timestamp"] = record.asctime
        log_record["service_name"] = "Assignments"
        log_record["log_level"] = record.levelname
        log_record["request_id"] = get_request_id()
        log_record["message_body"] = record.message


