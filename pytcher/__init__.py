from collections import namedtuple


# module , clazz, method
_annotated_routes = {}

AnnotatedRoute = namedtuple('AnnotatedRoute', ['path', 'command', 'func'])


class NotFoundException(Exception):
    pass


def route(path, method='GET'):
    def decorator_add_route(func):
        tokens = func.__qualname__.split('.')
        _annotated_routes[func.__module__] = _annotated_routes.get(func.__module__, {})
        # decorated function or method inside class
        clazz = tokens[0] if len(tokens) == 2 else None
        _annotated_routes[func.__module__][clazz] = _annotated_routes.get(clazz, [])
        _annotated_routes[func.__module__][clazz].append(AnnotatedRoute(path, method, func))

    return decorator_add_route


Response = namedtuple('Response', ['body', 'status_code', 'headers'])
Response.__new__.__defaults__ = (None, 200, {})


from pytcher.app import App  # noqa: F401
from pytcher.request import Request  # noqa: F401
from pytcher.router import Router  # noqa: F401
from pytcher.matchers import *  # noqa: F401,E402,F403
