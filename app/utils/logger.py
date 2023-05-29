import logging
import uuid

import flask


def get_request_id():
    """
    Returns the current request ID or a new one if there is none
    In order of preference:
    * If we've already created a request ID and stored it in the flask.g context local, use that
    * If a client has passed in the X-Request-Id header, create a new ID with that prepended
    * Otherwise, generate a request ID and store it in flask.g.request_id
    :return:
    """
    if getattr(flask.g, 'request_id', None):
        return flask.g.request_id

    if not flask.has_request_context():
        return uuid.uuid4()

    headers = flask.request.headers
    request_id = headers.get("X-Request-Id")
    if not request_id:
        request_id = uuid.uuid4()

    flask.g.request_id = request_id

    return request_id


class RequestIdFilter(logging.Filter):
    """
    This is a logging filter that makes the request ID available for use in
    the logging format. Note that we're checking if we're in a request
    context, as we may want to log things before Flask is fully loaded.
    """
    def filter(self, record):
        record.request_id = get_request_id() if flask.has_request_context() else ''
        return True