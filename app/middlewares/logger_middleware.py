import logging

from flask import request

from app import logger


def log_request_info():
    if logger.isEnabledFor(logging.INFO):
        logger.info(request.headers)
        logger.info(request.get_json(silent=True))


def log_response_info(response):
    if logger.isEnabledFor(logging.INFO):
        logger.info(response.data)
    return response
