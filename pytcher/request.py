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
        self._command_stack = []
        self._remaining_stack = list(reversed(url.split('/')[1:]))  # skip first '/'
        self._header_stack = []

    def __str__(self):
        return '[Request: command={command} url={url}]'.format(
            command=self.command,
            url=self.url
        )

    def __repr__(self):
        return self.__str__()

    def end(self, *args):
        return RequestMatch(self, not self._remaining_stack, [], [])

    def get(self, *args):
        is_match = self.command == self.GET
        return RequestMatch(self, is_match, [], [])

    def put(self, *args):
        is_match = self.command == self.PUT
        return RequestMatch(self, is_match, [], [])

    def post(self, *args):
        is_match = self.command == self.POST
        return RequestMatch(self, is_match, [], [])

    def patch(self, *args):
        is_match = self.command == self.PATCH
        return RequestMatch(self, is_match, [], [])

    def delete(self, *args):
        is_match = self.command == self.DELETE
        return RequestMatch(self, is_match, [], [])

    def path(self, *path_elements):
        matched_path, matched_vars = self.match_path(self._remaining_stack, path_elements)
        print('========>', matched_path, path_elements, self._remaining_stack)
        return RequestMatch(self, matched_path != [], matched_path, matched_vars, self._remaining_stack[:-len(matched_path)])

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

    def _enter(self, path_matched, command):
        for e in path_matched:
            self._remaining_stack.pop()
            self._path_stack.append(e)

        if command:
            self._command_stack.append(command)

    def _exit(self, path_matched, command):
        for e in path_matched:
            self._path_stack.pop()
            self._remaining_stack.append(e)

        if command:
            self._command_stack.pop()


class ParameterOperator(object):
    def __init__(self, key, parameter_dict):
        self._key = key
        self._parameter_dict = parameter_dict


class RequestHeader(object):

    def __getattribute__(self, key):
        pass


class SkipWithBlock(Exception):
    pass


class RequestMatch(object):
    def __init__(self, request, is_match, matched_path, matched_vars, remaining_path=None, command=None):
        self._request = request
        self._is_match = is_match
        self._matched_path = matched_path
        self._matched_vars = matched_vars
        self._remaining_path = remaining_path
        self._command=command

    def __enter__(self):
        # If it's a match, execute normally otherwise skip what is inside the with context
        if self._is_match:
            self._request._enter(self._matched_path, self._command)
            return self._matched_vars
        else:
            sys.settrace(lambda *args, **keys: None)
            frame = sys._getframe(1)

            def trace(frame, event, arg):
                raise SkipWithBlock()

            frame.f_trace = trace

    def __exit__(self, type, value, traceback):
        if type is None:
            self._request._exit(self._matched_path, self._command)
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

class InvalidPathValue(Exception):
    pass