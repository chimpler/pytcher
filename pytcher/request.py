import sys
from pytcher import to_type, is_type

class Request(object):
    def __init__(self, command, url, headers):
        self.url = url
        self.headers = headers
        self.command = command
        self._path_stack = []
        self._command_stack = []
        self._remaining_stack = list(reversed(url.split('/')[1:]))  # skip first '/'
        self.current_command = None
        self._header_stack = []

    def __str__(self):
        return 'e'

    def __repr__(self):
        return '[' +']'

    def end(self, *args):
        return RequestMatch(self, not self._remaining_stack, [], [])

    def path(self, *args):
        matched_path, matched_vars = self.matched_path(args)
        return RequestMatch(self, matched_path != [], matched_path, matched_vars)

    def matched_path(self, path_elements):
        if len(path_elements) > len(self._remaining_stack):
            return [], []

        # TODO: accept captures of multiple segments at once
        # TODO: accept Regexp
        matched_path = []
        matched_vars = []

        for p_elt, r_elt in zip(path_elements, reversed(self._remaining_stack)):
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

            matched_path.append(p_elt)

        return matched_path, matched_vars

    def _enter(self, path_matched):
        for e in path_matched:
            self._remaining_stack.pop()
            self._path_stack.append(e)

    def _exit(self, path_matched):
        for e in path_matched:
            self._path_stack.pop()
            self._remaining_stack.append(e)


class SkipWithBlock(Exception):
    pass

class RequestMatch(object):
    def __init__(self, request, is_match, matched_path, matched_vars):
        self._request = request
        self._is_match = is_match
        self._matched_path = matched_path
        self._matched_vars = matched_vars

    def __enter__(self):
        # If it's a match, execute normally otherwise skip what is inside the with context
        if self._is_match:
            self._request._enter(self._matched_path)
            return self._matched_vars
        else:
            sys.settrace(lambda *args, **keys: None)
            frame = sys._getframe(1)
            frame.f_trace = self.trace

    def trace(self, frame, event, arg):
        raise SkipWithBlock()

    def __exit__(self, type, value, traceback):
        self._request._exit(self._matched_path)

        if type is None:
            return  # No exception
        if issubclass(type, SkipWithBlock):
            return True  # Suppress special SkipWithBlock exception

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass