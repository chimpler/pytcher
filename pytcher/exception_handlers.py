import logging
import traceback
from abc import abstractmethod

from pytcher.request import Request


logger = logging.getLogger(__name__)


class ExceptionHandler(object):
    @abstractmethod
    def handle(self, request: Request, exception: Exception):
        pass


class DefaultDebugExceptionHandler(ExceptionHandler):
    def handle(self, request: Request, exception: Exception):
        stack = traceback.extract_stack()[:-3] + traceback.extract_tb(exception.__traceback__)  # add limit=??

        return {
            'message': str(exception),
            'request': {
                'url': request.url
            },
            'stacktrace': traceback.format_list(stack)
        }


class DefaultExceptionHandler(ExceptionHandler):
    def handle(self, request: Request, exception: Exception):
        stack = traceback.extract_stack()[:-3] + traceback.extract_tb(exception.__traceback__)  # add limit=??

        logging.error('Exception %s: %s', exception, traceback.format_list(stack))
        return {
            'message': 'Internal Error'
        }
