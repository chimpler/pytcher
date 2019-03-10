import logging
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

from pytcher import _version

logger = logging.getLogger('pytcher')


class LocalWebserver(object):
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

    def start(
            self,
            request_handler,
            interface='0.0.0.0',
            port=8000,
            server_class=HTTPServer
    ):
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
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len) if content_len else None

                parse_result = urllib.parse.urlparse(self.path)
                response = request_handler(self.command, parse_result.path, parse_result.query, self.headers, body)
                self.send_response(response.status_code)
                for header_key, header_value in response.headers.items():
                    self.send_header(header_key, header_value)
                self.end_headers()

                # TODO replace by using iterator
                self.wfile.write(response.message.encode('utf-8'))

        self.motd()
        print('Started server http://{host}:{port}'.format(host=interface, port=port))
        httpd = server_class((interface, port), HTTPRequestHandler)
        httpd.serve_forever()