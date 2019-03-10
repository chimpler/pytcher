import json
import logging
import os
import traceback
import urllib

from pytcher import NotFoundException, Response
from pytcher.request import Request
from pytcher.webservers import LocalWebserver

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


class App(object):
    def __init__(self,
                 route_handler,
                 output_serializer=json.dumps,
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

    def start(self, interface='0.0.0.0', port=8000):
        if not self._has_wsgi:
            LocalWebserver().start(self._handle_request, interface, port)

    def _handle_request(self, command, uri, query_string, headers, payload):
        try:
            params = urllib.parse.parse_qs(query_string) if query_string else {}
            request = Request(command, uri, params, headers, payload)
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

        return Response(self._output_serializer(output), status_code, headers)