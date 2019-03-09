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
    for book_id, admin_id in r / 'admin' / 'books' / Regex('c.*r') / 'admin' / Integer():
        for _ in r.get | r.put:
            for _ in r.h['X-Organization'] == 'chimpler':
                return {'book': {'id': book_id, 'admin_id': admin_id}}

            return {'message': 'restricted access'}

        for _ in r.post:
            return {'books': [{'id': 2}]}

    for novel_id in r.get / 'novels' / Integer():
        for author_id in (r / 'authors' / Integer()) & (r.p['g'] == 3):
            return {'novel': novel_id, 'author': author_id}


if __name__ == '__main__':
    # App().start(route_handler, exception_handler=exception_handler)
    App().start(route_handler)
