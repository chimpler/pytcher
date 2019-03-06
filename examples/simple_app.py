from pytcher import App, Request
import contextlib

def exception_handler(request: Request, e: Exception):
    pass

def route_handler(r: Request):

    with r / 'books' / int as [book_id]:
        with r.get | r.put:
            return {'book': {'id': book_id}}

        with r.post:
            return {'books': [{'id': 2}]}

    with (r.get / 'novels' / int / 'authors' / int) & (r.p('g') == '3') as [novel_id, author_id]:
        print(r.p('g').list())
        return {'novel': novel_id, 'author': author_id}


if __name__ == '__main__':
    App().start(route_handler)
