import re
from abc import abstractmethod
from datetime import datetime
from itertools import zip_longest
from typing import List

import pytcher


def to_type(new_type, n):
    try:
        return new_type(n)
    except ValueError:
        return NoMatch


def is_type(new_type, n):
    try:
        new_type(n)
        return True
    except ValueError:
        return False


class InvalidValue(object):
    pass


class NoMatch(object):
    pass


class PathMatcher(object):
    @abstractmethod
    def match(self, value):
        pass


class Integer(PathMatcher):
    __slots__ = ['min', 'max']

    def __init__(self, min=None, max=None):
        super(PathMatcher, self).__init__()
        self.min = min
        self.max = max

    def match(self, value):
        int_value = to_type(int, value)
        if int_value == NoMatch:
            return NoMatch

        if self.min:
            if self.min > int_value:
                return NoMatch

        if self.max:
            if self.max < int_value:
                return NoMatch

        return int_value


class Float(PathMatcher):
    __slots__ = []

    def __init__(self, min=None, max=None):
        super(PathMatcher, self).__init__()
        self.min = min
        self.max = max

    def match(self, value):
        float_value = to_type(float, value)
        if float_value == NoMatch:
            return NoMatch

        if self.min:
            if self.min > float_value:
                return NoMatch

        if self.max:
            if self.max < float_value:
                return NoMatch

        return float_value


class String(PathMatcher):
    __slots__ = []

    def match(self, value):
        return value


class Choice(PathMatcher):
    __slots__ = ['ignore_case', 'choices']

    def __init__(self, *choices, ignore_case=True):
        self.choices = choices
        self.ignore_case = ignore_case

    def match(self, value):
        for choice in self.choices:
            if self.ignore_case:
                if choice.lower() == value.lower():
                    return choice
            elif choice == value:
                return choice

        return NoMatch


class Date(PathMatcher):
    __slots__ = ['format']

    def __init__(self, format: str = '%Y-%m-%d'):
        self._format = format

    def match(self, value):
        return datetime.strptime(value, self._format).date()


class DateTime(PathMatcher):
    __slots__ = ['format']

    def __init__(self, format: str = '%Y-%m-%dT%H:%M:%s'):
        self._format = format

    def match(self, value):
        return datetime.strptime(value, self._format)


class Regex(PathMatcher):
    __slots__ = ['format', 'flags', 'data_types']

    def __init__(self, format: str, flags: int = 0, data_types: List = []):
        self._pattern = re.compile(format, flags)
        self._data_types = data_types
        self._flags = flags

    def match(self, value):
        m = self._pattern.match(value)
        if m:
            if m.groups():
                values = [
                    pytcher.convert_type(data_type, group) if data_type else group
                    for group, data_type in zip_longest(m.groups(), self._data_types)
                ]
                return values[0] if len(values) == 1 else values
            else:
                return value
        else:
            return NoMatch

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[Regex pattern='{pattern}' flags='{flags}' types={types}]".format(
            pattern=self._pattern,
            flags=self._flags,
            types=self._data_types
        )
