import http
import logging
import os
import urllib
from typing import Dict, Union, Callable, List, Type
from wsgiref.simple_server import make_server

from pytcher import NotFoundException, Response, _version
from pytcher.exception_handlers import ExceptionHandler, DefaultDebugExceptionHandler, DefaultExceptionHandler
from pytcher.marshallers import Marshaller, DefaultJSONMarshaller
from pytcher.request import Request
from pytcher.router import Router
from pytcher.unmarshallers import DefaultJSONUnmarshaller

logger = logging.getLogger(__name__)


class App(object):
    def __init__(self,
                 router: Union[Router, Callable],
                 marshallers: Dict[Type, Marshaller] = None,
                 unmarshallers: Dict[Type, Marshaller] = None,
                 exception_handlers: List[Union[Router, Callable]] = None,
                 debug: bool = True):

        self._route_handler = router.route if isinstance(router, Router) else router
        assert callable(self._route_handler), 'router must be a callable or of type Router'

        self._debug = debug

        if marshallers:
            self._marshallers = marshallers
        else:
            self._marshallers = {dict: DefaultJSONMarshaller().marshall}

        if unmarshallers:
            self._unmarshallers = unmarshallers
        else:
            self._unmarshallers = {dict: DefaultJSONUnmarshaller().unmarshall}

        if exception_handlers:
            self._exception_handler = [
                exception_handler.handle if isinstance(exception_handler, ExceptionHandler) else exception_handler
                for exception_handler in exception_handlers
            ]
        else:
            self._exception_handler = [
                DefaultDebugExceptionHandler().handle if debug else DefaultExceptionHandler().handle
            ]

        wsgi_version = os.environ.get('wsgi.version')
        if wsgi_version:
            logger.info('Using WSGI {version}'.format(version='.'.join(wsgi_version)))
            self._has_wsgi = True
        else:
            self._has_wsgi = False

    def motd(self):
        print(r"""             _       _
 _ __  _   _| |_ ___| |__   ___ _ __
| '_ \| | | | __/ __| '_ \ / _ \ '__|
| |_) | |_| | || (__| | | |  __/ |
| .__/ \__, |\__\___|_| |_|\___|_|
|_|    |___/
v{app_version} built on {build_on} ({commit})
""".format(
            app_version=_version.app_version,
            build_on=_version.built_at,
            commit=_version.git_version
        )
        )

    def start(self, interface='0.0.0.0', port=8000):
        self.motd()
        if not self._has_wsgi:
            server = make_server(interface, port, self)
            server.serve_forever()
            # LocalWebserver().start(self._handle_request, interface, port)

    def _handle_request(self, command: str, uri: str, query_string: str, headers: Dict[str, str], body: str):
        try:
            params = urllib.parse.parse_qs(query_string) if query_string else {}
            request = Request(command, uri, params, headers, body, self._unmarshallers)
            route_output = self._route_handler(request)
            if route_output is None:
                raise NotFoundException()
        except Exception as e:
            route_output = next(
                (
                    handler(e, request)
                    for handler in self._exception_handlers
                ),
                None
            )

        headers = {}
        output_and_status_code = route_output
        if isinstance(output_and_status_code, tuple):
            output, status_code = output_and_status_code
        elif isinstance(output_and_status_code, Response):
            output = output_and_status_code.message
            status_code = output_and_status_code.status_code
            headers = output_and_status_code.headers
        else:
            output = output_and_status_code
            status_code = http.HTTPStatus.OK

        return Response(self._marshallers[dict](output), status_code, headers)

    def __call__(self, environ, start_response):
        # Replace HTTP_ABC=value to ABC=value
        headers = {
            key[5:]: value
            for key, value in environ.items()
            if key.startswith('HTTP_')
        }

        body_size = environ.get('CONTENT_LENGTH')
        body = environ['wsgi.input'].read(int(body_size)) if body_size else None

        # improve to read data in stream
        response = self._handle_request(
            environ['REQUEST_METHOD'],
            environ['PATH_INFO'],
            environ['QUERY_STRING'],
            headers,
            body
        )

        status_response = '{status_code} {status_message}'.format(
            status_code=response.status_code,
            status_message=http.HTTPStatus(response.status_code).name
        )

        start_response(status_response, list(response.headers.items()))

        return [response.body.encode('utf-8')]
