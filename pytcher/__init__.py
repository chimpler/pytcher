import re
from collections import namedtuple

# module , clazz, method
_annotated_routes = {}

AnnotatedRoute = namedtuple('AnnotatedRoute', ['path', 'command', 'func'])


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
                replacement = r'(?P<{name}>.+?)'.format(name=name)
            elif data_type:
                src = r'<{type}:{name}>'.format(type=data_type, name=name)

                if data_type == 'string':
                    data_type = 'str'
                    replacement = r'(?P<{name}>.+?)'.format(name=name)
                elif data_type == 'int':
                    replacement = r'(?P<{name}>[+-]?\d+?)'.format(name=name)
                elif data_type == 'float':
                    replacement = r'(?P<{name}>[-+]?([0-9]*\.[0-9]+|[0-9]+)?)'.format(name=name)

            current_res = current_res.replace(src, replacement)
            data_types.append(data_type)
        return Regex(current_res, data_types=data_types)
    else:
        return current_res


def convert_str_to_path_elements(path_elt):
    return [
        gen_path_regex(elt)
        for elt in path_elt.strip('/').split('/')
    ]


def route(path, method='GET'):
    def decorator_add_route(func):
        print(func)
        tokens = func.__qualname__.split('.')
        if func.__module__ not in _annotated_routes:
            _annotated_routes[func.__module__] = {}
        # decorated function or method inside class
        clazz = tokens[0] if len(tokens) == 2 else None

        if clazz not in _annotated_routes[func.__module__]:
            _annotated_routes[func.__module__][clazz] = []

        _annotated_routes[func.__module__][clazz].append(
            AnnotatedRoute(convert_str_to_path_elements(path), method, func)
        )
        print(_annotated_routes)
        return func

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


Response = namedtuple('Response', ['body', 'status_code', 'headers'])
Response.__new__.__defaults__ = (None, 200, {})

from pytcher.app import App  # noqa: F401
from pytcher.request import Request  # noqa: F401
from pytcher.router import Router  # noqa: F401
from pytcher.matchers import *  # noqa: F401,E402,F403
