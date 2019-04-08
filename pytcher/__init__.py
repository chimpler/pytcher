import re
from abc import abstractmethod
from collections import namedtuple

# module , clazz, method
from typing import Callable

_annotated_routes = {}
_annotated_exceptions = {}

AnnotatedRoute = namedtuple('AnnotatedRoute', ['path', 'command', 'func'])
AnnotatedExceptionHandler = namedtuple('AnnotatedExceptionHandler', ['exception', 'func'])


class Router(object):

    @abstractmethod
    def route(self, r):
        pass

    def handle_exception(self, r, e: Exception):
        pass


class NotFoundException(Exception):
    pass


RE_PATH_ELT = re.compile(r'<(?:(?P<type>.+?):)?(?P<name>.+?)>')


def gen_path_regex(elt):
    current_res = elt
    groups = RE_PATH_ELT.findall(elt)
    data_types = []
    if groups:
        for data_type, name in groups:
            if not data_type:
                src = r'<{name}}>'.format(type=data_type, name=name),
                replacement = r'(?P<{name}>.+)'.format(name=name)
            elif data_type:
                src = r'<{type}:{name}>'.format(type=data_type, name=name)

                if data_type == 'string':
                    data_type = 'str'
                    replacement = r'(?P<{name}>.+)'.format(name=name)
                elif data_type == 'int':
                    replacement = r'(?P<{name}>[+-]?\d+)'.format(name=name)
                elif data_type == 'float':
                    replacement = r'(?P<{name}>[-+]?([0-9]*\.[0-9]+|[0-9]+)?)'.format(name=name)

            current_res = current_res.replace(src, replacement)
            data_types.append(data_type)
        return Regex(current_res, data_types=data_types)
    else:
        return current_res


def convert_str_to_path_elements(path):
    if not path:
        return []

    return [
        gen_path_regex(elt)
        for elt in path.strip('/').split('/')
    ]


def handle_exception(exception_or_function=Exception):
    def decorator_add_exception_handler(func):
        tokens = func.__qualname__.split('.')
        if func.__module__ not in _annotated_exceptions:
            _annotated_exceptions[func.__module__] = {}
        # decorated function or method inside class
        clazz = tokens[0] if len(tokens) == 2 else None

        if clazz not in _annotated_exceptions[func.__module__]:
            _annotated_exceptions[func.__module__][clazz] = []

        _annotated_exceptions[func.__module__][clazz].append(
            AnnotatedExceptionHandler(exception_or_function, func)
        )
        return func

    if not isinstance(exception_or_function, Callable) and issubclass(exception_or_function, Exception):  # If called as @handle_exception with parenthesis
        func = exception_or_function
        exception_or_function = Exception
        return decorator_add_exception_handler(func)
    else:  # If called as @handle_exception with no parenthesis
        return decorator_add_exception_handler


def route(path_or_function=None, method='GET'):
    def decorator_add_route(func):
        tokens = func.__qualname__.split('.')
        if func.__module__ not in _annotated_routes:
            _annotated_routes[func.__module__] = {}
        # decorated function or method inside class
        clazz = tokens[0] if len(tokens) == 2 else None

        if clazz not in _annotated_routes[func.__module__]:
            _annotated_routes[func.__module__][clazz] = []

        _annotated_routes[func.__module__][clazz].append(
            AnnotatedRoute(convert_str_to_path_elements(path_or_function), method, func)
        )

        return func

    if isinstance(path_or_function, Callable):  # If called as @route with no parenthesis
        func = path_or_function
        path_or_function = None
        return decorator_add_route(func)
    else:  # If called as @route with parenthesis
        return decorator_add_route


def convert_type(data_type, value):
    if data_type == 'int':
        return int(value)
    elif data_type == 'float':
        return float(value)
    elif data_type in 'boolean':
        return value.lower() not in ('false', 'f', '0')
    else:
        return value


def get_routers(router):
    if isinstance(router, Callable):  # annotated functions
        found = next(
            (
                annotated_route
                for annotated_route in _annotated_routes.get(router.__module__, {}).get(None, [])
                if router.__name__ == annotated_route.func.__name__
            ),
            []
        )
        return [found] if found else []
    else:  # annotated methods in classes
        return [
            AnnotatedRoute(path, command, getattr(router, func.__name__))
            for path, command, func in
            _annotated_routes.get(router.__module__, {}).get(type(router).__name__, [])
        ]


def run_router(request, router):
    for matched_vars in request.path(*router.path):
        return router.func(request, *matched_vars)


def get_exception_handlers(exception_handler):
    if isinstance(exception_handler, Callable):
        found = next(
            (
                annotated_exception_handler
                for annotated_exception_handler in _annotated_exceptions.get(exception_handler.__module__, {}).get(None)
                if exception_handler.__name__ == annotated_exception_handler.func.__name__
            ),
            []
        )
        return [found] if found else []
    else:
        return [
            AnnotatedExceptionHandler(exception, getattr(exception_handler, func.__name__))
            for exception, func in
            _annotated_exceptions.get(exception_handler.__module__, {}).get(type(exception_handler).__name__, [])
        ]


Response = namedtuple('Response', ['body', 'status_code', 'headers'])
Response.__new__.__defaults__ = (None, 200, {})

from pytcher.app import App  # noqa: F401
from pytcher.request import Request  # noqa: F401
from pytcher.matchers import *  # noqa: F401,E402,F403
