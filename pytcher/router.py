from abc import abstractmethod
from typing import List

from pytcher import AnnotatedRoute
from pytcher.request import Request


class Router(object):

    @abstractmethod
    def route(self, r):
        pass

    def handle_exception(self, r, e: Exception):
        pass


class AnnotatedRouter(Router):

    def __init__(self, router, annotated_routes: List[AnnotatedRoute]):
        self._router = router
        self._annotated_routes = annotated_routes

    def route(self, r: Request):
        for path, command, func in self._annotated_routes:
            if r.command == command:

                func(self._router, )