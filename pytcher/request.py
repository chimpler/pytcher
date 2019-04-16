import json
import sys
from abc import abstractmethod
from typing import Iterable, Tuple, List, Any, Dict

import pytcher
from pytcher import convert_str_to_path_elements, Url
from pytcher.matchers import is_type, NoMatch, PathMatcher, to_type
from pytcher.unmarshallers import Unmarshaller


class Request(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

    def __init__(
            self,
            command: str,
            url: Url,
            params: Dict[str, Any] = {},
            headers: Dict[str, Any] = {},
            content=None,
            unmarshaller: Unmarshaller = None):
        self.url = url
        self.headers = headers
        self.command = command
        self.params = params
        self._path_stack = []
        self._remaining_stack = list(reversed(url.path.lstrip('/').split('/'))) if url.path != '/' else []  # skip first '/'
        self._content = content
        self._unmarshaller = unmarshaller

    def __str__(self):
        return '[Request: command={command} url={url} host={host} port={port} path_stack={path_stack} remaining_stack={remaining_stack}]'.format(
            command=self.command,
            url=self.url,
            host=self.host,
            port=self.port,
            path_stack=self._path_stack,
            remaining_stack=self._remaining_stack
        )

    def __repr__(self):
        return self.__str__()

    @property
    def h(self):
        return ParameterDict(self, self.headers, HeaderOperator, True)

    @property
    def p(self):
        return ParameterDict(self, self.params, ParameterOperator)

    def route(self, routers):
        router_list = routers if isinstance(routers, Iterable) else [routers]
        router_handlers = [
            r
            for router in router_list
            for r in pytcher.get_routers(router)
        ]

        return next(
            (
                output
                for output in (
                    pytcher.run_router(self, router)
                    for router in router_handlers
                )
                if output is not None
            ),
            None
        )

    def entity(self, obj_type, json_path='$'):
        return self._unmarshaller(obj_type, self._content)

    @property
    def json(self):
        return json.loads(self._content)

    @property
    def end(self):
        return RequestMatch(self, not self._remaining_stack, self._remaining_stack)

    @property
    def get(self):
        return RequestMatch(self, self.command == self.GET, self._remaining_stack)

    @property
    def put(self):
        return RequestMatch(self, self.command == self.PUT, self._remaining_stack)

    @property
    def post(self):
        return RequestMatch(self, self.command == self.POST, self._remaining_stack)

    @property
    def patch(self):
        return RequestMatch(self, self.command == self.PATCH, self._remaining_stack)

    @property
    def delete(self):
        return RequestMatch(self, self.command == self.DELETE, self._remaining_stack)

    def path(self, *path_elements):
        if not path_elements:
            return RequestMatch(self, True, self._remaining_stack, [], [])

        transformed_elements = [
            sub_elt
            for path_elt in path_elements
            for sub_elt in (convert_str_to_path_elements(path_elt) if isinstance(path_elt, str) else [path_elt])
        ]

        matched_path, matched_vars = self.match_path(self._remaining_stack, transformed_elements)
        return RequestMatch(self, matched_path != [], self._remaining_stack[:-len(matched_path)], matched_path,
                            matched_vars)

    def root(self):
        pass

    def param(self, key, value, comp_function=lambda x, y: x == y):
        # TODO create built-in functions
        pass

    @classmethod
    def match_path(cls, remaining_stack: List[Any], path_elements: List[Any]) -> Tuple[List[Any], List[Any]]:
        if path_elements == [None] and not remaining_stack:
            return [None], []

        if len(path_elements) > len(remaining_stack):
            return [], []

        # TODO: accept captures of multiple segments at once
        matched_path = []
        matched_vars = []

        for p_elt, r_elt in zip(path_elements, reversed(remaining_stack)):
            if type(p_elt).__name__ == 'type':
                value = p_elt().match(r_elt)
                if value == NoMatch:
                    return [], []
                else:
                    matched_vars.append(value)
            elif isinstance(p_elt, PathMatcher):
                value = p_elt.match(r_elt)
                if value == NoMatch:
                    return [], []
                else:
                    matched_vars.append(value)
            elif isinstance(p_elt, str) and p_elt == r_elt:
                pass
            elif isinstance(p_elt, int) and p_elt == to_type(int, r_elt):
                pass
            elif isinstance(p_elt, float) and p_elt == to_type(float, r_elt):
                pass
            elif p_elt == str:
                matched_vars.append(r_elt)
            elif p_elt == int and is_type(int, r_elt):
                matched_vars.append(int(r_elt))
            elif p_elt == float and is_type(float, r_elt):
                matched_vars.append(float(r_elt))
            else:
                return [], []

            matched_path.append(r_elt)

        return matched_path, matched_vars

    def __truediv__(self, other):
        return self.path(other)

    def _enter(self, path_matched):
        for e in path_matched:
            if e is not None:
                self._remaining_stack.pop()
                self._path_stack.append(e)

    def _exit(self, path_matched):
        for e in path_matched:
            if e is not None:
                self._path_stack.pop()
                self._remaining_stack.append(e)


class ParameterDict(object):
    __slots__ = ['_request', '_parameters', '_parameter_operator_clazz', '_ignore_case']

    def __init__(self, request, parameters, parameter_operator_clazz, ignore_case=False):
        self._request = request
        self._parameters = {k.lower(): v for k, v in parameters.items()} if ignore_case else parameters
        self._parameter_operator_clazz = parameter_operator_clazz
        self._ignore_case = ignore_case

    def __getitem__(self, key):
        final_key = key.lower() if self._ignore_case else key
        return self._parameter_operator_clazz(self._request, self._parameters.get(final_key))

    def __getattr__(self, key):
        return self.__getitem__(key)

    def get(self, key, default=None):
        final_key = key.lower() if self._ignore_case else key
        return self._parameter_operator_clazz(self._request, self._parameters.get(final_key, default))

    def has(self, key):
        final_key = key.lower() if self._ignore_case else key
        return RequestMatch(self._request, final_key in self._parameters)

    def hasnot(self, key):
        final_key = key.lower() if self._ignore_case else key
        return RequestMatch(self._request, final_key not in self._parameters)


class AbstractParameterOperator(object):
    __slots__ = ['_request', '_value']

    def __init__(self, request, value):
        self._request = request
        self._value = value

    def __eq__(self, other):
        return RequestMatch(self._request, self._convert(other) == other)

    def __lt__(self, other):
        return RequestMatch(self._request, self._convert(other) < other)

    def __le__(self, other):
        return RequestMatch(self._request, self._convert(other) <= other)

    def __gt__(self, other):
        return RequestMatch(self._request, self._convert(other) > other)

    def __ge__(self, other):
        return RequestMatch(self._request, self._convert(other) >= other)

    def __ne__(self, other):
        return RequestMatch(self._request, self._convert(other) != other)

    def __contains__(self, item):
        return RequestMatch(self._request, item in self._value)

    @abstractmethod
    def _convert(self, other):
        pass


class ParameterOperator(AbstractParameterOperator):
    __slots__ = ['_request', '_value']

    def __init__(self, request, value):
        super(ParameterOperator, self).__init__(request, value)

    def _convert(self, other):
        if self._value is None:
            return None
        elif isinstance(other, int):
            return int(self._value[-1])
        elif isinstance(other, float):
            return float(self._value[-1])
        elif isinstance(other, list):
            return list(self._value)
        elif isinstance(other, set):
            return set(self._value)
        else:
            return self._value[-1]

    @property
    def str(self):
        return self._value[-1] if self._value else None

    @property
    def int(self):
        return int(self._value[-1]) if self._value else None

    @property
    def float(self):
        return float(self._value[-1]) if self._value else None

    @property
    def list(self):
        return self._value if self._value else None


class HeaderOperator(AbstractParameterOperator):
    __slots__ = ['_request', '_value']

    def __init__(self, request, value):
        super(HeaderOperator, self).__init__(request, value)

    def _convert(self, other):
        if self._value is None:
            return None
        elif isinstance(other, int):
            return int(self._value)
        elif isinstance(other, float):
            return float(self._value)
        else:
            return self._value

    @property
    def str(self):
        return self._value

    @property
    def int(self):
        return int(self._value)

    @property
    def float(self):
        return float(self._value)


class SkipWithBlock(Exception):
    pass


class RequestMatch(object):
    __slots__ = ['_request', '_is_match', '_remaining_path', '_matched_path', '_matched_vars', '_first_time']

    def __init__(self, request: Request, is_match: bool, remaining_path: List = [], matched_path: List = [], matched_vars: List = []):
        self._request = request
        self._is_match = is_match
        self._remaining_path = list(remaining_path)
        self._matched_path = list(matched_path)
        self._matched_vars = list(matched_vars)
        self._first_time = True

    def __enter__(self):
        # If it's a match, execute normally otherwise skip what is inside the with context
        if self._is_match:
            self._request._enter(self._matched_path)
            if len(self._matched_vars) == 1:
                return self._matched_vars[0]
            else:
                return self._matched_vars
        else:
            sys.settrace(lambda *args, **keys: None)
            frame = sys._getframe(1)

            def trace(frame, event, arg):
                raise SkipWithBlock()

            frame.f_trace = trace

    def __exit__(self, type, value, traceback):
        if type is None:
            self._request._exit(self._matched_path)
            return  # No exception
        if issubclass(type, SkipWithBlock):
            return True  # Suppress special SkipWithBlock exception

    def __and__(self, other):
        self._matched_vars += other._matched_vars if other._is_match else []
        self._is_match &= other._is_match
        return self

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        if self._is_match:
            return self
        elif other._is_match:
            return other
        else:
            return self

    def __ror__(self, other):
        return self.__ror__(other)

    def __truediv__(self, other):
        matched_path, matched_var = Request.match_path(self._remaining_path, [other])
        if matched_path:
            if matched_path != [None]:
                self._matched_vars += matched_var
                self._matched_path.insert(0, self._remaining_path.pop())
        else:
            self._is_match = False

        return self

    def __repr__(self):
        return '[RequestMatch request={request}, is_match={is_match}, ' \
               'remaining_path=[{remaining_path}], matched_path=[{matched_path}], ' \
               'matched_vars=[{matched_vars}]]'.format(
                   request=self._request,
                   is_match=self._is_match,
                   remaining_path=', '.join(self._remaining_path),
                   matched_path=', '.join([str(s) for s in self._matched_path]),
                   matched_vars=', '.join([str(s) for s in self._matched_vars]))

    def __iter__(self):
        self._first_time = True
        return self

    def __next__(self):
        if self._is_match:
            if self._first_time:
                self._request._enter(self._matched_path)
                self._first_time = False
                if len(self._matched_vars) == 1:
                    return self._matched_vars[0]
                else:
                    return self._matched_vars
            else:
                self._request._exit(self._matched_path)
                raise StopIteration
        else:
            raise StopIteration

    @property
    def is_match(self):
        return self._is_match


class InvalidPathValue(Exception):
    pass
