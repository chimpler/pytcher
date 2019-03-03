from http.server import HTTPServer, BaseHTTPRequestHandler
from pytcher.request import Request
import json


class App(object):
    def start(self, route_handler, interface='0.0.0.0', port=5000, server_class=HTTPServer, output_serializer=json.dumps):
        class HTTPRequestHandler(BaseHTTPRequestHandler):
            def call_method(self, command):
                request = Request(command, self.path, self.headers)
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

            def do_GET(self):
                return self.call_method(self.command)

        httpd = server_class((interface, port), HTTPRequestHandler)
        httpd.serve_forever()


def route_handler(r):
    with r.path('authors'):
        return {'authors': []}

    with r.path('books'):
        with r.path(int) as book_id:
            return {'book': {'id': book_id}}

        with r.end():
            return {'books': [{'id': 2}]}

App().start(route_handler)