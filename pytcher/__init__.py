import re
from collections import namedtuple
from dataclasses import dataclass
from functools import reduce
from typing import Callable, Iterable

from pytcher.matchers import Regex

_annotated_routes = {}
_annotated_exceptions = {}

AnnotatedRoute = namedtuple('AnnotatedRoute', ['path', 'command', 'func'])
AnnotatedExceptionHandler = namedtuple('AnnotatedExceptionHandler', ['exception', 'func'])


class NotFoundException(Exception):
    pass


class RouteException(Exception):
    pass


class UnmarshallException(Exception):
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


def handle_exception(exception=Exception):
    def decorator_add_exception_handler(func):
        if func.__module__ not in _annotated_exceptions:
            _annotated_exceptions[func.__module__] = {}
        # decorated function or method inside class

        cur_elt = _annotated_exceptions[func.__module__]
        tokens = func.__qualname__.split('.')
        num_tokens = len(tokens)
        for index, token in enumerate(tokens):
            if index == num_tokens - 1:
                cur_elt[token] = AnnotatedExceptionHandler(exception, func)
            else:
                if token not in cur_elt:
                    cur_elt[token] = {}
        return func

    if not isinstance(exception, Callable) and issubclass(exception,
                                                          Exception):  # If called as @handle_exception with parenthesis
        func = exception
        exception = Exception
        return decorator_add_exception_handler(func)
    else:  # If called as @handle_exception with no parenthesis
        return decorator_add_exception_handler


def route(path=None, prefix=None, method=None):
    def decorator_add_route(func):
        # path can be a path or the function itself if the annotation is simply @route
        # decorated function or method inside class
        cur_elt = _annotated_routes
        tokens = [func.__module__] + func.__qualname__.split('.')
        num_tokens = len(tokens)
        for index, token in enumerate(tokens):
            if index == num_tokens - 1:
                if path and prefix:
                    raise RouteException('path and prefix cannot be both set')

                route_path = convert_str_to_path_elements(path if path else prefix)
                cur_elt[token] = AnnotatedRoute(route_path, method, func)
            else:
                if token not in cur_elt:
                    cur_elt[token] = {}

            cur_elt = cur_elt[token]
        return func

    if isinstance(path, Callable):  # If called as @route with no parenthesis
        func = path
        path = None
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


# TODO: combine get_routers and get_exception_handlers
def get_routers(router):
    def get_annotated_routes(route_dict):
        return [
            route
            for key, value in route_dict.items()
            for route in ([value] if isinstance(value, AnnotatedRoute) else get_annotated_routes(value))
        ]

    if isinstance(router, Callable):
        path_tokens = [router.__module__] + router.__qualname__.split('.')
    else:
        router_type = type(router)
        path_tokens = [router_type.__module__] + router_type.__qualname__.split('.')

    obj_dict = reduce(
        lambda d, x: d.get(x, {}),
        path_tokens,
        _annotated_routes
    )
    return [
        AnnotatedRoute(
            path,
            command,
            func if isinstance(router, Callable)
            else getattr(router, func.__name__)
        )
        for path, command, func in (
            [obj_dict] if isinstance(obj_dict, AnnotatedRoute)
            else get_annotated_routes(obj_dict)
        )
    ]


@dataclass
class Url(object):
    scheme: str = 'http'
    host: str = 'localhost'
    port: int = 80
    script: str = ''
    path: str = '/'
    query_string: str = ''

    @classmethod
    def from_environ(cls, environ):
        scheme = environ['wsgi.url_scheme']

        server_host_port = environ.get('HTTP_HOST').split(':')
        if len(server_host_port) == 2:
            host = server_host_port[0]
            port = int(server_host_port[1])
        else:
            host = server_host_port[0]
            port = 80 if scheme == 'http' else 443

        return cls(
            scheme,
            host,
            port,
            environ['SCRIPT_NAME'],
            environ['PATH_INFO'],
            environ['QUERY_STRING']
        )

    @property
    def url(self):
        return '{scheme}://{host}{port}{script_name}{path_info}{query_string}'.format(
            scheme=self.scheme,
            host=self.host,
            port=(':' + str(self.port)) if (self.scheme == 'http' and self.port != 80 or self.port != 443) else '',
            script_name=self.script,
            path_info=self.path,
            query_string=('?' + self.query_string) if self.query_string else ''
        )

    @property
    def host_url(self):
        return '{scheme}://{host}{port}/'.format(
            scheme=self.scheme,
            host=self.host,
            port=(':' + str(self.port)) if (self.scheme == 'http' and self.port != 80 or self.port != 443) else ''
        )


from pytcher.request import Request  # noqa E402


def run_router(request: Request, route: AnnotatedRoute):
    if route.command:
        if isinstance(route.command, Iterable):
            if request.command not in route.command:
                return None
            elif request.command != route.command:
                return None

    for matched_vars in request.path(*route.path):
        return route.func(request, *matched_vars)


def get_exception_handlers(handler_exception):
    def get_exception_handlers(handler_dict):
        return [
            handler_exception
            for key, value in handler_dict.items()
            for handler_exception in
            ([value] if isinstance(value, AnnotatedExceptionHandler) else get_exception_handlers(value))
        ]

    if isinstance(handler_exception, Callable):
        path_tokens = [handler_exception.__module__] + handler_exception.__qualname__.split('.')
    else:
        handler_type = type(handler_exception)
        path_tokens = [handler_type.__module__] + handler_type.__qualname__.split('.')

    handler_dict = reduce(
        lambda d, x: d.get(x, {}),
        path_tokens,
        _annotated_exceptions
    )
    return [
        AnnotatedExceptionHandler(
            exception,
            func
            if isinstance(func, Callable)
            else getattr(handler_exception, func.__name__)
        )
        for exception, func in (
            [handler_dict] if isinstance(handler_dict, AnnotatedExceptionHandler)
            else get_exception_handlers(handler_dict)
        )
    ]


Response = namedtuple('Response', ['body', 'status_code', 'headers'])
Response.__new__.__defaults__ = (None, 200, {})

from pytcher.app import App  # noqa: F401
from pytcher.request import Request, Request, Request  # noqa: F401
from pytcher.matchers import *  # noqa: F401,E402,F403
