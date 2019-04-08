import http
import logging
import os
import urllib
from typing import Callable, Dict, Iterable, List, Union
from wsgiref.simple_server import make_server

import pytcher
from pytcher import _version, NotFoundException, Response
from pytcher.defaults import debug_exception_handler, default_exception_handler
from pytcher.marshallers import Marshaller
from pytcher.marshallers.csv_marshaller import CSVMarshaller
from pytcher.marshallers.json_marshaller import JSONMarshaller
from pytcher.marshallers.xml_marshaller import XMLMarshaller
from pytcher.request import Request
from pytcher.unmarshallers import Unmarshaller
from pytcher.unmarshallers.json_unmarshaller import JSONUnmarshaller

logger = logging.getLogger(__name__)


class App(object):

    def __init__(self,
                 handlers: Union[List, Callable] = [],
                 marshallers: Dict[str, Marshaller] = None,
                 unmarshallers: Dict[str, Unmarshaller] = None,
                 debug: bool = True):
        handler_list = (
            handlers if isinstance(handlers, Iterable) else [handlers]
        ) + [
            debug_exception_handler if debug else default_exception_handler
        ]

        self._routers = [
            r
            for router in handler_list
            for r in pytcher.get_routers(router)
        ]


        self._exception_handlers = [
                                       e
                                       for exception_handler in handler_list
                                       for e in pytcher.get_exception_handlers(exception_handler)
                                   ]

        print(self._exception_handlers)
        for router in self._routers:
            logger.debug('Registered router %s', router.func.__name__)

        for exception_handler in self._exception_handlers:
            logger.debug('Registered exception handler %s', exception_handler.func.__name__)

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
                'application/json': JSONUnmarshaller().unmarshall
            }

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
{debug}
""".format(
            app_version=_version.app_version,
            build_on=_version.built_at,
            commit=_version.git_version,
            debug='\n***WARNING: DEBUG is set to true. DISABLE IT FOR PRODUCTION ***' if self._debug else ''
        )
        )

    def start(self, interface='0.0.0.0', port=8000):
        self.motd()
        if not self._has_wsgi:
            server = make_server(interface, port, self)
            server.serve_forever()

    def _handle_request(self, command: str, uri: str, query_string: str, headers: Dict[str, str], body: str):
        # convert to charset
        content_type = headers.get('CONTENT_TYPE', 'application/json')
        unmarshaller = self._unmarshallers[content_type]
        params = urllib.parse.parse_qs(query_string) if query_string else {}
        request = Request(command, uri, params, headers, body, unmarshaller)
        try:
            route_output = next(
                (
                    output
                    for output in (
                        pytcher.run_router(request, router)
                        for router in self._routers
                    )
                    if output is not None
                )
                , None
            )

            if route_output is None:
                raise NotFoundException()
        except Exception as e:
            route_output = next(
                (
                    handler(e, request)
                    for exception_type, handler in self._exception_handlers
                    if isinstance(e, exception_type)
                ),
                None
            )

        output_and_status_code = route_output
        accept_type = headers.get('ACCEPT', 'application/json').lower()
        if isinstance(output_and_status_code, tuple):
            output, status_code = output_and_status_code
        elif isinstance(output_and_status_code, Response):
            output = output_and_status_code.message
            status_code = output_and_status_code.status_code
            headers = output_and_status_code.headers
        else:
            output = output_and_status_code
            status_code = http.HTTPStatus.OK

        if accept_type in self._marshallers:
            marshaller = self._marshallers[accept_type]
        else:
            return Response('Accept {type} not supported'.format(type=accept_type), http.HTTPStatus.NOT_ACCEPTABLE)
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
