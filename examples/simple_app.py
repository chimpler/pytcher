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
    with r / 'books' / Regex('c.*r') as [book_id]:
        with r.get | r.put:
            with r.h.has('X-Organization-Id'):
                return {'book': {'id': book_id}}
            with r.h.hasnot('X-Organization-Id'):
                return {'message': 'restricted access'}

        with r.post:
            return {'books': [{'id': 2}]}

    with (r.get / 'novels' / Integer() / 'authors' / Integer()) & (r.p['g'] == 3) as [novel_id, author_id]:
        print(r.p['g'].int)
        return {'novel': novel_id, 'author': author_id}


if __name__ == '__main__':
    App().start(route_handler, exception_handler=exception_handler)
