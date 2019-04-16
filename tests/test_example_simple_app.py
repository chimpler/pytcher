import http
import logging

from pytcher import App, Request, Url

import examples.simple_app


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class TestSimpleApp(object):
    app = App(examples.simple_app.MyRouter())

    def test_get_all(self):
        response = self.app._handle_request(Request.GET, Url(path='/items'))
        assert http.HTTPStatus.OK == response.status_code
        assert '["pizza","cheese","ice-cream","butter"]' == response.body

    def test_get_one(self):
        response = self.app._handle_request(Request.GET, Url(path='/items/1'))
        assert http.HTTPStatus.OK == response.status_code
        assert '"cheese"' == response.body

    def test_post(self):
        response = self.app._handle_request(Request.POST, Url(path='/items'), body='"banana"')
        assert http.HTTPStatus.CREATED == response.status_code
        assert '"banana"' == response.body

        response = self.app._handle_request(Request.GET, Url(path='/items'))
        assert http.HTTPStatus.OK == response.status_code
        assert '["pizza","cheese","ice-cream","butter","banana"]' == response.body
