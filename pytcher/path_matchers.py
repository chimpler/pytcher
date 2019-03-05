from abc import abstractmethod

def to_type(new_type, n):
    try:
        return new_type(n)
    except Exception as e:
        return InvalidValue

def is_type(new_type, n):
    try:
        new_type(n)
        return True
    except Exception as e:
        return False


class InvalidValue(object):
    pass


class PathMatcher(object):
    @abstractmethod
    @classmethod
    def match(cls, value):
        pass


class IntNumber(object):
    def match(self, value):
        return True

class Choice(object):
    def __init__(self, *choices, ignore_case):
        self.choices = choices
        self.ignore_case = ignore_case

class Date(object):
    def __init__(self, format):
        # TODO
        pass

class DateTime(object):
    def __init__(self, format):
        # TODO
        pass

class Regex(object):
    def __init__(self, format):
        # TODO
        pass

