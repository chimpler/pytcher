import http
from pytcher import App, Request
from examples.app_with_annotation import MyRouter


def test_simple_with():
    app = App(MyRouter())
    response = app._handle_request(Request.GET, '/items')
    assert http.HTTPStatus.OK == response.status_code
    # assert '["pizza","cheese","ice-cream","butter"]' == response.body
