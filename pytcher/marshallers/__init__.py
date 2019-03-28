import datetime
from abc import abstractmethod


class Marshaller(object):

    @abstractmethod
    def marshall(self, obj):
        pass


# TODO add more
default_encoders = [
    (lambda x: isinstance(x, datetime.datetime) and x.tzinfo is None, lambda x: x.strformat('%Y-%m-%dT%H:%M:%S.%f')),
    (lambda x: isinstance(x, datetime.datetime) and x.tzinfo is not None, lambda x: x.strformat('%Y-%m-%dT%H:%M:%S.%f%z')),
    (lambda x: isinstance(x, datetime.date), lambda x: 5),
    (lambda x: isinstance(x, datetime.time), lambda x: 7),
    (lambda x: isinstance(x, datetime.timezone), lambda x: 7),
    (lambda x: isinstance(x, datetime.tzinfo), lambda x: 7)
]


class MarshallerException(Exception):
    pass