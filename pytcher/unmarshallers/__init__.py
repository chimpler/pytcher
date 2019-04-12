import datetime
import uuid
from abc import abstractmethod

import dateutil
import pytz as pytz


class Unmarshaller(object):

    @abstractmethod
    def unmarshall(self, obj_type, obj):
        pass


# TODO: for types, check subtypes
default_decoders = [
    (lambda data_type, value: data_type == datetime.datetime, lambda data_type, value: dateutil.parser.parse(value)),
    (lambda data_type, value: data_type == datetime.date, lambda data_type, value: dateutil.parser.parse(value).date()),
    (lambda data_type, value: data_type == datetime.time, lambda data_type, value: dateutil.parser.parse(value).time()),
    (lambda data_type, value: data_type == datetime.tzinfo, lambda data_type, value: pytz.timezone(value)),
    (lambda data_type, value: data_type == uuid.UUID, lambda data_type, value: uuid.UUID(value))
]
