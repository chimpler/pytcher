import datetime
import re
import uuid
from abc import abstractmethod
from enum import Enum

import dateutil.parser
import pytz as pytz


RE_TIMEDELTA = re.compile(r'(?:P(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d*(?:\.\d+)?)S)?)')

class Unmarshaller(object):

    @abstractmethod
    def unmarshall(self, obj_type, obj):
        pass

def parse_timedelta(value: str):
    match = RE_TIMEDELTA.match(value)
    if match:
        return datetime.timedelta(
            **{
                k: float(v)
                for k, v in match.groupdict('0').items()
            }
        )
    else:
        return None

# TODO: for types, check subtypes
default_decoders = [
    (lambda data_type, value: issubclass(data_type, Enum), lambda data_type, value: getattr(data_type, value, None)),
    (lambda data_type, value: issubclass(data_type,  datetime.datetime), lambda data_type, value: dateutil.parser.parse(value)),
    (lambda data_type, value: issubclass(data_type, datetime.date), lambda data_type, value: dateutil.parser.parse(value).date()),
    (lambda data_type, value: issubclass(data_type, datetime.time), lambda data_type, value: dateutil.parser.parse(value).time()),
    (lambda data_type, value: issubclass(data_type, datetime.timezone), lambda data_type, value: pytz.timezone(value)),
    (lambda data_type, value: issubclass(data_type, datetime.timedelta), lambda data_type, value: parse_timedelta(value)),
    (lambda data_type, value: issubclass(data_type, uuid.UUID), lambda data_type, value: uuid.UUID(value))
]


def decode(obj_type, value, extra_decoders=[]):
    return next(
        (
            decode(obj_type, value)
            for condition, decode in extra_decoders + default_decoders
            if condition(obj_type, value)
        ),
        value
    )
