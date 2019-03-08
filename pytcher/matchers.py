from abc import abstractmethod
from datetime import datetime
import re


def to_type(new_type, n):
    try:
        return new_type(n)
    except Exception as e:
        return NoMatch


def is_type(new_type, n):
    try:
        new_type(n)
        return True
    except Exception as e:
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
    def match(self, value):
        return to_type(int, value)


class Float(PathMatcher):
    def match(self, value):
        return to_type(float, value)


class String(PathMatcher):
    def match(self, value):
        return value


class Choice(PathMatcher):
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
    def __init__(self, format='%Y-%m-%d'):
        self._format = format

    def match(self, value):
        return datetime.strptime(value, self._format).date()


class DateTime(PathMatcher):
    def __init__(self, format='%Y-%m-%dT%H:%M:%s'):
        self._format = format

    def match(self, value):
        return datetime.strptime(value, self._format)


class Regex(PathMatcher):
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
