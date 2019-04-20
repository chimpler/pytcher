import datetime
import uuid
from abc import abstractmethod
from enum import Enum
from typing import Callable, List, Tuple


def format_timedelta(d: datetime.timedelta):
    result = ''
    if d.days != 0:
        result += 'P' + str(d.days) + 'D'

    if d.seconds or d.microseconds:
        result += 'T'
        total_seconds = int(d.total_seconds()) % 86400
        hours = int(total_seconds // 3600)
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60 + (d.microseconds / 1000000)
        if hours:
            result += str(hours) + 'H'
        if minutes:
            result += str(minutes) + 'M'
        if seconds:
            result += str(seconds) + 'S'

    return result


# TODO add more
default_encoders = [
    (lambda x: isinstance(x, Enum), lambda x: x.name),
    (lambda x: isinstance(x, datetime.datetime) and x.tzinfo is None, lambda x: x.strftime('%Y-%m-%dT%H:%M:%S.%f')),
    (lambda x: isinstance(x, datetime.datetime) and x.tzinfo is not None,
     lambda x: x.strftime('%Y-%m-%dT%H:%M:%S.%f%z')),
    (lambda x: isinstance(x, datetime.date), lambda x: x.strftime('%Y-%m-%d')),
    (lambda x: isinstance(x, datetime.time), lambda x: x.strftime('%H:%M:%S.%f')),
    # (lambda x: isinstance(x, datetime.tzinfo), lambda x: '{hour}{minute}'.format(x.seconds / 3600, x.seconds % 3600)),
    (lambda x: isinstance(x, datetime.tzinfo), lambda x: x.zone),
    (lambda x: isinstance(x, datetime.timedelta), format_timedelta),
    (lambda x: isinstance(x, uuid.UUID), lambda x: str(x))
]


def encode(obj, extra_encoders=[]):
    return next(
        (
            encode(obj)
            for condition, encode in extra_encoders + default_encoders
            if condition(obj)
        )
    )


class Marshaller(object):

    def __init__(self, encoders: List[Tuple[Callable, Callable]] = default_encoders):
        self._encoders = encoders

    @abstractmethod
    def marshall(self, obj):
        pass


class MarshallerException(Exception):
    pass
