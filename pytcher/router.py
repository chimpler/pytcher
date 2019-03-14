from abc import abstractmethod


class Router(object):

    @abstractmethod
    def route(self, r):
        pass

    def handle_exception(self, r, e: Exception):
        pass
