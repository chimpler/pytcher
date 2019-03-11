import json
from abc import abstractmethod

from pytcher import Response
from pytcher.defaults import debug_exception_handler
from pytcher.request import Request


class AppRouter(object):

    @abstractmethod
    def route(self, r: Request):
        pass

    def serialize(self, obj, status_code, headers):
        return Response(json.dumps(obj), status_code, headers)

    def handle_exception(self, r: Request, e: Exception):
        return debug_exception_handler(r, e)
