import json
from abc import abstractmethod

from pytcher import Request
from pytcher.app import debug_exception_handler, App


class AppRouter(object):

    @abstractmethod
    def route(self, r: Request):
        pass

    def serialize(self, obj):
        return json.dumps(obj)

    def handle_exception(self, r: Request, e: Exception):
        return debug_exception_handler(r, e)

    # For WSGI
    def __call__(self, environ, start_fn):
        start_fn('200 OK', [('Content-Type', 'text/plain')])
        yield "Hello World!\n"

    def start(self, interface='0.0.0.0', port=8000):
        App(
            route_handler=self.route,
            exception_handler=self.handle_exception,
            output_serializer=self.serialize
        ).start(interface, port)
