from http.server import HTTPServer, BaseHTTPRequestHandler
from pytcher.request import Request
import json
import logging
from pytcher import _version, NotFoundException
import traceback
import urllib.parse

logger = logging.getLogger('pytcher')


def debug_exception_handler(request, exception):
    logger.info(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return 'Page not found', 404
    else:
        return 'Internal Error: {exception}\n{stack_trace}'.format(exception=exception, stack_trace=traceback.format_exc()), 500


def default_exception_handler(request, exception):
    logger.info(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return 'Page not found', 404
    else:
        return 'Internal Error', 500

class App(object):
    def motd(self):
        print(
"""
             _       _
 _ __  _   _| |_ ___| |__   ___ _ __ 
| '_ \| | | | __/ __| '_ \ / _ \ '__|
| |_) | |_| | || (__| | | |  __/ |   
| .__/ \__, |\__\___|_| |_|\___|_|   
|_|    |___/                         

v{app_version} built on {build_on} ({commit})
{debugger_message}
""".format(
    app_version=_version.app_version,
    build_on=_version.built_at,
    commit=_version.git_version,
    debugger_message='\n***WARNING: DEBUG MODE IS ON!' if self._debug else ''
)
        )

    def start(
        self,
        route_handler,
        interface='0.0.0.0',
        port=8000,
        server_class=HTTPServer,
        output_serializer=json.dumps,
        exception_handler=None,
        debug=True
    ):
        self._debug = debug
        if exception_handler is None:
            exception_handler = debug_exception_handler if debug else default_exception_handler

        class HTTPRequestHandler(BaseHTTPRequestHandler):
            def __init__(self, request, client_address, server):
                super(HTTPRequestHandler, self).__init__(request, client_address, server)


            def do_GET(self):
                return self.call_command()

            def do_POST(self):
                return self.call_command()

            def do_PUT(self):
                return self.call_command()

            def do_PATCH(self):
                return self.call_command()

            def do_DELETE(self):
                return self.call_command()

            def call_command(self):
                try:
                    parse_result = urllib.parse.urlparse(self.path)
                    params = urllib.parse.parse_qs(parse_result.query) if parse_result.query else {}
                    request = Request(self.command, parse_result.path, self.headers, params)
                    route_output = route_handler(request)

                    if route_output is None:
                        raise NotFoundException()
                    else:
                        output_and_status_code = route_output
                        if isinstance(output_and_status_code, tuple):
                            output, status_code = output_and_status_code
                        else:
                            output = output_and_status_code
                            status_code = 200
                except Exception as e:
                    output, status_code = exception_handler(request, e)

                serialized_output = output_serializer(output)
                self.send_response(status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(serialized_output.encode('utf-8'))

        self.motd()
        print('Started server http://{host}:{port}'.format(host=interface, port=port))
        httpd = server_class((interface, port), HTTPRequestHandler)
        httpd.serve_forever()
