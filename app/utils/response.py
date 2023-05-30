from flask import make_response

from app.utils.logger import get_request_id


class Response:
    HTTP_SUCCESS = 200
    HTTP_ACCEPTED = 202
    HTTP_MOVED_PERMANENTLY = 301
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403
    HTTP_NOT_FOUND = 404
    HTTP_ERROR = 500
    HTTP_NOT_IMPLEMENTED = 501

    def __init__(self, data=None, status=None):
        self.data = data
        self.status = status

    def build(self):
        response = {
            'status': self.status,
            'payload': self.data,
            'correlation_id': get_request_id()
        }
        resp = make_response(response)

        return resp

    @staticmethod
    def make(data, status, deprecation_warning=False, deprecation_date=None):
        response = {
            'status': status,
            'payload': data,
            'correlation_id': get_request_id()
        }
        if deprecation_warning:
            deprecation_message = 'This endpoint is deprecated and will be removed in the future.'
            if deprecation_date:
                deprecation_message += f' This endpoint will be removed on {deprecation_date}.'
            response['deprecation_warning'] = deprecation_message
        resp = make_response(response, status)
        return resp