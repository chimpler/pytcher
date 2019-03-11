from abc import abstractmethod
from datetime import datetime
import re


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
    __slots__ = []

    def match(self, value):
        return to_type(int, value)


class Float(PathMatcher):
    __slots__ = []

    def match(self, value):
        return to_type(float, value)


class String(PathMatcher):
    __slots__ = []

    def match(self, value):
        return value


class Choice(PathMatcher):
    __slots__ = ['ignore_case', 'choices']

    def __init__(self, ignore_case=True, *choices):
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

    def __init__(self, format='%Y-%m-%d'):
        self._format = format

    def match(self, value):
        return datetime.strptime(value, self._format).date()


class DateTime(PathMatcher):
    __slots__ = ['format']

    def __init__(self, format='%Y-%m-%dT%H:%M:%s'):
        self._format = format

    def match(self, value):
        return datetime.strptime(value, self._format)


class Regex(PathMatcher):
    __slots__ = ['format', 'flags']

    def __init__(self, format, flags=0):
        self._pattern = re.compile(format, flags)

    def match(self, value):
        m = self._pattern.match(value)
        if m:
            if m.groups():
                return list(m.groups())
            else:
                return value
        else:
            return NoMatch
