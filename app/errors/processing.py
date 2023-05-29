from app.errors.base import BaseAPIException


class ProcessingException(BaseAPIException):
    def __init__(self, messages, *args: object) -> None:
        super().__init__(messages, *args)