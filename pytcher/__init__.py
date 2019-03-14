from collections import namedtuple


class NotFoundException(Exception):
    pass


Response = namedtuple('Response', ['body', 'status_code', 'headers'])
Response.__new__.__defaults__ = (None, 200, {})


from pytcher.app import App  # noqa: F401
from pytcher.request import Request  # noqa: F401
from pytcher.router import Router  # noqa: F401
from pytcher.matchers import *  # noqa: F401,E402,F403
