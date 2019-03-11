import http
import json
import traceback

from pytcher import NotFoundException, Response
import logging


logger = logging.getLogger(__name__)


def debug_exception_handler(request, exception):
    logger.info(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return 'Page not found', http.HTTPStatus.NOT_FOUND
    else:
        return 'Internal Error: {exception}\n{stack_trace}'.format(exception=exception,
                                                                   stack_trace=traceback.format_exc()), http.HTTPStatus.INTERNAL_SERVER_ERROR


def default_exception_handler(request, exception):
    logger.info(exception, exc_info=True)
    if isinstance(exception, NotFoundException):
        return 'Page not found', http.HTTPStatus.NOT_FOUND
    else:
        return 'Internal Error', http.HTTPStatus.INTERNAL_SERVER_ERROR


def default_json_serializer(obj, status_code=None, headers={}):
    final_status_code = status_code if status_code else http.HTTPStatus.OK.value
    final_headers = {
        **headers,
        **{
            'Content-Type': 'application/json'
        }
    }
    return Response(json.dumps(obj), final_status_code, final_headers)
