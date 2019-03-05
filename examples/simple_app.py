from pytcher import App

def exception_handler(request, e):
    pass

def route_handler(r):

    with r.path('authors'):
        return {'authors': []}

    with r / 'novels' / int / 'authors' / int as [novel_id, author_id]:
        return {'novel': novel_id, 'author': author_id}

    with r.path('books'):
        with r.path(int) as [book_id]:
            with r.get():
                return {'book': {'id': book_id}}

            with r.post():
                return {'posts': []}

        with r.end():
            return {'books': [{'id': 2}]}


if __name__ == '__main__':
    App().start(route_handler)