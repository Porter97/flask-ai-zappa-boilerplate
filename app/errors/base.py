
class BaseAPIException(Exception):
    messages = None

    def __init__(self, messages, *args: object) -> None:
        super().__init__(*args)
        self.messages = messages

    def get_message(self):
        return self.messages
