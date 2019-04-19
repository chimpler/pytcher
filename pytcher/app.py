import http
import logging
import os
import subprocess
import sys
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
from pytcher.watcher import Watcher

logger = logging.getLogger(__name__)


class App(object):

    def __init__(self,
                 handlers: Union[List, Callable] = [],
                 marshallers: Dict[str, Marshaller] = None,
                 unmarshallers: Dict[str, Unmarshaller] = None,
                 debug: bool = True):
        """
        :param handlers: function/class or list of functions/classes that are decorated with @route
        :param marshallers: dictionary of marshallers to use for conversion from input data to python object. By default it supports `application/json`
        :param unmarshallers: dictionary of marshallers to use for conversion from python object to output. By default it supports `application/json`
        :param debug: if debug is enabled, it will use a simple web server and allow autoreload
        """
        self._server = None
        self._process = None
        self._debug = debug

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

        for router in self._routers:
            logger.debug('Registered router %s', router.func.__name__)

        for exception_handler in self._exception_handlers:
            logger.debug('Registered exception handler %s', exception_handler.func.__name__)

        if marshallers:
            self._marshallers = marshallers
        else:
            csv_marshaller = CSVMarshaller()
            json_marshaller = JSONMarshaller()
            self._marshallers = {
                'application/json': json_marshaller.marshall,
                'application/xml': XMLMarshaller().marshall,
                'text/csv': csv_marshaller.marshall,
                'application/csv': csv_marshaller.marshall,
                '*/*': json_marshaller.marshall
            }

        if unmarshallers:
            self._unmarshallers = unmarshallers
        else:
            json_unmarshaller = JSONUnmarshaller()
            self._unmarshallers = {
                'application/json': json_unmarshaller.unmarshall,
                'text/plain': json_unmarshaller.unmarshall,
                '*/*': json_unmarshaller.unmarshall
            }

        wsgi_version = os.environ.get('wsgi.version')
        if wsgi_version:
            logger.info('Using WSGI {version}'.format(version='.'.join(wsgi_version)))
            self._has_wsgi = True
        else:
            self._has_wsgi = False

    def motd(self, autoreload=False):
        print(r"""             _       _
 _ __  _   _| |_ ___| |__   ___ _ __
| '_ \| | | | __/ __| '_ \ / _ \ '__|
| |_) | |_| | || (__| | | |  __/ |
| .__/ \__, |\__\___|_| |_|\___|_|
|_|    |___/
v{app_version} built on {build_on} ({commit})
{debug}
{autoreload}
""".format(
            app_version=_version.app_version,
            build_on=_version.built_at,
            commit=_version.git_version,
            debug='\n*** WARNING: DEBUG is set to true. DISABLE IT FOR PRODUCTION ***' if self._debug else '',
            autoreload='*** Autoreload is on' if autoreload else ''
        )
        )

    def start(self, interface: str = '0.0.0.0', port: int = 8000, autoreload: bool = True):
        """
        Start the web server if it is not run from a WSGI server, otherwise it does not do anything
        :param interface: listening address (default is 0.0.0.0)
        :param port: listening port (default 8000)
        :param autoreload: if set to true, the server restarts j vpfppppp--- 9iiiooyh6ytwhen a file is updated in the current directory (default True)
        :return:
        """
        if not self._has_wsgi:
            # run a new process with watchdog
            if self._debug and autoreload and '__PYTCHER_CHILD_PROCESS__' not in os.environ:
                watcher = Watcher(self)
                watcher.start()
                while True:
                    self._process = subprocess.Popen(['python', *sys.argv], env={**os.environ, '__PYTCHER_CHILD_PROCESS__': '1'})
                    self._process.wait()
            else:
                self.motd(autoreload)
                self._server = make_server(interface, port, self)
                self._server.serve_forever()

    def restart(self):
        logger.info('File change detected. Restarting app...')
        if self._process:
            self._process.kill()

    def stop(self):
        if self._server:
            logger.info('Shutting down...')
            self._server.shutdown()

    def _handle_request(
            self,
            command: str,
            url: pytcher.Url,
            headers: Dict[str, str] = {},
            body: str = ''
    ):
        # convert to charset
        content_type = headers.get('CONTENT_TYPE') or 'application/json'

        unmarshaller = self._unmarshallers[content_type]
        params = urllib.parse.parse_qs(url.query_string) if url.query_string else {}
        request = Request(command, url, params, headers, body, unmarshaller)
        try:
            route_output = next(
                (
                    output
                    for output in (
                        pytcher.run_router(request, router)
                        for router in self._routers
                    )
                    if output is not None
                ),
                None
            )

            if route_output is None:
                raise NotFoundException()
        except Exception as e:
            route_output = next(
                (
                    handler(request, e)
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

    @property
    def route_handlers(self):
        return self._routers

    @property
    def exception_handlers(self):
        return self._exception_handlers

    def __call__(self, environ, start_response):
        # Replace HTTP_ABC=value to ABC=value
        # TODO: filter some values
        headers = {
            key[5:] if key.startswith('HTTP_') else key: value
            for key, value in environ.items()
        }

        body_size = environ.get('CONTENT_LENGTH')
        body = environ['wsgi.input'].read(int(body_size)) if body_size else None

        url = pytcher.Url.from_environ(environ)
        # improve to read data in stream
        response = self._handle_request(
            environ['REQUEST_METHOD'],
            url,
            headers,
            body
        )

        status_response = '{status_code} {status_message}'.format(
            status_code=response.status_code,
            status_message=http.HTTPStatus(response.status_code).name
        )
        start_response(status_response, [])
        return [response.body.encode('utf-8')]
