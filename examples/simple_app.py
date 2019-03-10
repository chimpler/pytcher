# flake8: noqa: E999
from pytcher import App, Request, NotFoundException, Integer, Regex
import http


def exception_handler(request: Request, e: Exception):
    if isinstance(e, NotFoundException):
        return {
            'error': 'Page not found',
            'url': request.url
        }, http.client.NOT_FOUND
    else:
        return {
            'error': 'Internal error',
            'details': str(e)
        }, http.client.INTERNAL_SERVER_ERROR


def route_handler(r: Request):
    with r / 'admin' / 'books' / Regex('c.*r') / 'admin' / Integer() as [book_id, admin_id]:
        with r.get | r.put:
            with r.h['X-Organization'] == 'chimpler':
                return {'book': {'id': book_id, 'admin_id': admin_id}}

            return {'message': 'restricted access'}

        with r.post:
            return {'books': [{'id': 2}]}

    with r.get / 'novels' / Integer() as [novel_id]:
        with (r / 'authors' / Integer()) & (r.p['g'] == 3) as [author_id]:
            return {'novel': novel_id, 'author': author_id}

        return {'tools': [1, 2, 3]}


if __name__ == '__main__':
    App().start(route_handler, exception_handler=exception_handler)
