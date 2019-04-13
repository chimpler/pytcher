import http
import json
import logging
import traceback

from pytcher import handle_exception, NotFoundException, Response
from pytcher.request import Request

logger = logging.getLogger(__name__)


@handle_exception(Exception)
def debug_exception_handler(request: Request, exception: Exception):
    logger.info(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return {'error': 'Page not found'}, http.HTTPStatus.NOT_FOUND
    else:
        return {
            'error': str(exception),
            'url': request.url,
            'headers': {k: str(v) for k, v in request.headers.items()},
            'stack_trace': traceback.format_exc().split('\n')
        }, http.HTTPStatus.INTERNAL_SERVER_ERROR


@handle_exception(Exception)
def default_exception_handler(request: Request, exception: Exception):
    logger.error(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return {'error': 'Page not found'}, http.HTTPStatus.NOT_FOUND
    else:
        return {'error': 'Internal Error'}, http.HTTPStatus.INTERNAL_SERVER_ERROR


def default_json_serializer(obj, status_code=None, headers={}):
    final_status_code = status_code if status_code else http.HTTPStatus.OK.value
    final_headers = {
        'Content-Type': 'application/json',
        **headers,
    }
    return Response(json.dumps(obj), final_status_code, final_headers)
