class InvalidValue:
    pass

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

class NotFoundException(Exception):
    pass

from pytcher.app import App, Request
from pytcher.matchers import *