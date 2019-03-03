from http.server import HTTPServer, BaseHTTPRequestHandler
from pytcher.request import Request
import json
import logging
from pytcher import _version


logger = logging.getLogger('pytcher')


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
""".format(
    app_version=_version.app_version,
    build_on=_version.built_at,
    commit=_version.git_version
)
        )

    def start(self, route_handler, interface='0.0.0.0', port=5000, server_class=HTTPServer, output_serializer=json.dumps):
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
                request = Request(self.command, self.path, self.headers)
                route_output = route_handler(request)

                if route_output is None:
                    self.send_response(404)
                    serialized_output = 'Page not found'
                else:
                    serialized_output = output_serializer(route_output)
                    self.send_response(200)

                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(serialized_output.encode('utf-8'))

        self.motd()
        httpd = server_class((interface, port), HTTPRequestHandler)
        httpd.serve_forever()
