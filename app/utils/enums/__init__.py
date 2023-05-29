from enum import Enum


class ListableEnum(Enum):

    @classmethod
    def to_list(cls):
        return list(map(lambda c: c.value, cls))