from pytcher import App


def route_handler(r):

    with r.path('authors'):
        return {'authors': []}

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