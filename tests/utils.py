from contextlib import contextmanager


@contextmanager
def is_set(value=True):
    flag = Flag()
    yield flag
    assert flag.is_set() is value


class Flag(object):
    def __init__(self):
        self._value = False

    def set(self):
        self._value = True

    def is_set(self):
        return self._value
