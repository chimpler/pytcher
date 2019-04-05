import http
import logging
import os
import urllib
from typing import Callable, Dict, List, Union, Iterable
from wsgiref.simple_server import make_server

import pytcher
from pytcher import _version, NotFoundException, Response
from pytcher.exception_handlers import DefaultDebugExceptionHandler, DefaultExceptionHandler, ExceptionHandler
# from pytcher.marshallers import DefaultXMLMarshaller, Marshaller
from pytcher.marshallers import Marshaller
from pytcher.marshallers.csv_marshaller import CSVMarshaller
from pytcher.marshallers.json_marshaller import JSONMarshaller
from pytcher.marshallers.xml_marshaller import XMLMarshaller
from pytcher.request import Request
from pytcher.router import Router, AnnotatedRouter
from pytcher.unmarshallers import Unmarshaller
from pytcher.unmarshallers.json_unmarshaller import JSONUnmarshaller
import functools
from collections import namedtuple
from optparse import OptionParser
import inspect


logger = logging.getLogger(__name__)


class App(object):

    def __init__(self,
                 routers = [],
                 marshallers: Dict[str, Marshaller] = None,
                 unmarshallers: Dict[str, Unmarshaller] = None,
                 exception_handlers: List[Union[Router, Callable]] = None,
                 debug: bool = True):
        # self._annotated_routes = []

        def get_routers(router):
            if isinstance(router, Callable):
                found = next(
                    (
                        func
                        for func in pytcher._annotated_routes.get(router.__module__, {}).get(None)
                        if router.__name__ == func.__name__
                    ),
                    None
                )
                return [found] if found else []
            else:
                return pytcher._annotated_routes.get(router.__module__, {}).get(type(router).__name__)

        self._routers = [
            r
            for router in (routers if isinstance(routers, Iterable) else [routers])
            for r in get_routers(router)
        ]

        for router in self._routers:
            logger.debug('Registered router %s', router.func.__name__)

        # self._route_handler = router.route if isinstance(router, Callable) else router
        # assert callable(self._route_handler), 'router must be a callable or of type Router'

        self._debug = debug

        if marshallers:
            self._marshallers = marshallers
        else:
            csv_marshaller = CSVMarshaller()
            self._marshallers = {
                'application/json': JSONMarshaller().marshall,
                'application/xml': XMLMarshaller().marshall,
                'text/csv': csv_marshaller.marshall,
                'application/csv': csv_marshaller.marshall
            }

        if unmarshallers:
            self._unmarshallers = unmarshallers
        else:
            self._unmarshallers = {
                'application/json': JSONUnmarshaller().unmarshall,
                # 'application/xml': DefaultXMLUnmarshaller().unmarshall
            }

        if exception_handlers:
            self._exception_handlers = [
                exception_handler.handle if isinstance(exception_handler, ExceptionHandler) else exception_handler
                for exception_handler in exception_handlers
            ]
        else:
            self._exception_handlers = [
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
            # convert to charset
            content_type = headers.get('CONTENT_TYPE', 'application/json')
            unmarshaller = self._unmarshallers[content_type]
            request = Request(command, uri, params, headers, body, unmarshaller)

            route_output = next(
                (
                    router.func(request)
                    for router in self._routers
                )
                , None
            )

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

        output_and_status_code = route_output
        print(headers)
        accept_type = headers.get('ACCEPT', 'application/json')
        if isinstance(output_and_status_code, tuple):
            output, status_code = output_and_status_code
        elif isinstance(output_and_status_code, Response):
            output = output_and_status_code.message
            status_code = output_and_status_code.status_code
            headers = output_and_status_code.headers
        else:
            output = output_and_status_code
            status_code = http.HTTPStatus.OK

        marshaller = self._marshallers[accept_type]
        return Response(marshaller(output), status_code, headers)

    def __call__(self, environ, start_response):
        # Replace HTTP_ABC=value to ABC=value
        headers = {
            key[5:] if key.startswith('HTTP_') else key: value
            for key, value in environ.items()
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
        # list(response.headers.items())
        start_response(status_response, [])
        return [response.body.encode('utf-8')]
