from pytcher import route, Request


def test_simple_route():
    @route
    def test_route(r: Request):
        with r / 'items':
            return 1

        with r / 'books':
            return 2

