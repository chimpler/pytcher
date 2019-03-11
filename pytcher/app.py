import http
import json
import logging
import os
import traceback
import urllib
from typing import Dict
from wsgiref.simple_server import make_server
from pytcher import NotFoundException, Response, _version
from pytcher.request import Request


logger = logging.getLogger(__name__)


def debug_exception_handler(request, exception):
    logger.info(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return 'Page not found', 404
    else:
        return 'Internal Error: {exception}\n{stack_trace}'.format(exception=exception,
                                                                   stack_trace=traceback.format_exc()), 500


def default_exception_handler(request, exception):
    logger.info(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return 'Page not found', 404
    else:
        return 'Internal Error', 500


def default_json_serializer(obj, status_code=None, headers={}):
    # final_status_code = status_code if status_code else http.HTTPStatus.OK.value
    # final_headers = {
    #     **headers,
    #     **{
    #         'Content-Type': 'application/json'
    #     }
    # }
    # return Response(json.dumps(obj), final_status_code, final_headers)
    return Response(json.dumps(obj))

class App(object):
    def __init__(self,
                 route_handler,
                 output_serializer=default_json_serializer,
                 exception_handler=debug_exception_handler,
                 debug=True
                 ):
        self._route_handler = route_handler
        self._output_serializer = output_serializer
        self._exception_handler = exception_handler
        self._debug = debug

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
            request = Request(command, uri, params, headers, body)
            route_output = self._route_handler(request)
            if route_output is None:
                raise NotFoundException()
        except Exception as e:
            route_output = self._exception_handler(e, request)

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
            status_code = 200

        return self._output_serializer(output, status_code, headers)

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
