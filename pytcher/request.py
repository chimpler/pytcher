import sys
from pytcher import to_type, is_type

class Request(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

    def __init__(self, command, url, headers):
        self.url = url
        self.headers = headers
        self.command = command
        self._path_stack = []
        self._remaining_stack = list(reversed(url.split('/')[1:]))  # skip first '/'
        self._header_stack = []

    def __str__(self):
        return '[Request: command={command} url={url}]'.format(
            command=self.command,
            url=self.url
        )

    def __repr__(self):
        return self.__str__()

    def h(self, key):
        return ParameterOperator(self, self.headers.get(key))

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
        matched_path, matched_vars = self.match_path(self._remaining_stack, path_elements)
        return RequestMatch(self, matched_path != [], self._remaining_stack[:-len(matched_path)], matched_path, matched_vars)

    def root(self):
        pass

    def param(self, key, value, comp_function=lambda x,y: x == y):
        # TODO create built-in functions
        pass

    @classmethod
    def match_path(cls, remaining_stack, path_elements):
        # TODO maybe move to utility method
        # TODO optimize it
        if len(path_elements) > len(list(remaining_stack)):
            return [], []

        # TODO: accept captures of multiple segments at once
        # TODO: accept Regexp
        matched_path = []
        matched_vars = []

        for p_elt, r_elt in zip(path_elements, reversed(remaining_stack)):
            if isinstance(p_elt, str) and p_elt == r_elt:
                pass
            elif isinstance(p_elt, int) and p_elt == to_type(int, r_elt):
                pass
            elif isinstance(p_elt, float) and p_elt == to_type(float, r_elt):
                pass
            elif p_elt == str:
                pass
                matched_vars.append(r_elt)
            elif p_elt == int and is_type(int, r_elt):
                pass
                matched_vars.append(int(r_elt))
            elif p_elt == float and is_type(float, r_elt):
                matched_vars.append(float(r_elt))
            else:
                return [], []

            matched_path.append(r_elt)

        print('T======>', matched_path)
        return matched_path, matched_vars

    def __truediv__(self, other):
        return self.path(other)

    def _enter(self, path_matched):
        print('========')
        print(path_matched)
        print(self._remaining_stack)
        print('========')
        for e in path_matched:
            self._remaining_stack.pop()
            self._path_stack.append(e)

    def _exit(self, path_matched):
        for e in path_matched:
            self._path_stack.pop()
            self._remaining_stack.append(e)


class ParameterOperator(object):
    def __init__(self, request, value, negative=False):
        self._request = request
        self._value = value
        self._trans = lambda x: x if negative else not(x)

    def __eq__(self, other):
        return RequestMatch(self._request, self._trans(self._value == other))

    def __lt__(self, other):
        return RequestMatch(self._request, self._trans(self._value < other))

    def __le__(self, other):
        return RequestMatch(self._request, self._trans(self._value <= other))

    def __gt__(self, other):
        return RequestMatch(self._request, self._trans(self._value > other))

    def __ge__(self, other):
        return RequestMatch(self._request, self._trans(self._value >= other))

    def __ne__(self, other):
        return RequestMatch(self._request, self._trans(self._value != other))

    def __contains__(self, item):
        return RequestMatch(self._request, self._trans(item in self._value))

# class RequestHeader(object):
#
#     def __init__(self, request):
#         self._request = request
#
#     def __add__(self, key):
#         return ParameterOperator(self._request, self._request.headers.get(key))
#
#     def __sub__(self, key):
#         return ParameterOperator(self._request, self._request.headers.get(key), negative=True)


class SkipWithBlock(Exception):
    pass


class RequestMatch(object):
    def __init__(self, request, is_match, remaining_path=[], matched_path=[], matched_vars=[]):
        self._request = request
        self._is_match = is_match
        self._remaining_path = list(remaining_path)
        self._matched_path = list(matched_path)
        self._matched_vars = list(matched_vars)

    def __enter__(self):
        # If it's a match, execute normally otherwise skip what is inside the with context
        if self._is_match:
            self._request._enter(self._matched_path)
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
        return self(
            self._request,
            self._is_match and other.is_match,
            self._matched_path,
            self._matched_vars,
            self._command
        )

    def __or__(self, other):
        if self._is_match:
            return self
        elif other._is_match:
            return other

    def __truediv__(self, other):
        matched_path, matched_var = Request.match_path(self._remaining_path, [other])
        if matched_path:
            self._matched_path += [other]
            self._matched_vars += matched_var
            self._remaining_path.pop()
        else:
            self._is_match = False

        return self

    def __repr__(self):
        return '[RequestMatch request={request}, is_match={is_match}, remaining_path=[{remaining_path}], matched_path=[{matched_path}], matched_vars=[{matched_vars}]]'.format(
            request=self._request,
            is_match=self._is_match,
            remaining_path=', '.join(self._remaining_path),
            matched_path=', '.join([str(s) for s in self._matched_path]),
            matched_vars=', '.join([str(s) for s in self._matched_vars])
        )

class InvalidPathValue(Exception):
    pass