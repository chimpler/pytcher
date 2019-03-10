from collections import namedtuple


class NotFoundException(Exception):
    pass


Response = namedtuple('Response', ['message', 'status_code', 'headers'])
Response.__new__.__defaults__ = (None, 200, {})


from pytcher.app import LocalWebserver, Request  # noqa: F401
from pytcher.app_router import AppRouter  # noqa: F401
from pytcher.matchers import *  # noqa: F401,E402,F403
