from pytcher import Integer, Request
from tests.utils import is_set


def test_raw_request_matcher():
    request = Request(Request.GET, '/items/5')
    assert (request / 'items').is_match is True
    assert (request / 'books').is_match is False
    assert (request / 'items' / Integer()).is_match is True
    assert (request / 'items' / Integer).is_match is True
    assert (request / 'items' / None).is_match is False
    assert (request / 'items' / Integer / None).is_match is True


def test_raw_multiple_request_matcher():
    request = Request(Request.GET, '/books/1/pages/2')
    assert (request / 'books').is_match is True
    assert (request / 'books' / Integer).is_match is True
    assert (request / 'books' / Integer / 'pages').is_match is True
    assert (request / 'books' / Integer / 'pages' / Integer).is_match is True


def test_with_request_matcher():
    r = Request(Request.GET, '/items/5')

    with is_set() as flag:
        with r / 'items':
            flag.set()

    with is_set(False) as flag:
        with r / 'books':
            flag.set()

    with is_set() as flag:
        with r / 'items' / Integer() as item_id:
            assert 5 == item_id
            flag.set()

    with is_set() as flag:
        with r / 'items' / Integer as item_id:
            assert 5 == item_id
            flag.set()

    with is_set(False) as flag:
        with r / 'items' / None as item_id:
            assert 5 == item_id
            flag.set()

    with is_set() as flag:
        with r / 'items' / Integer / None as item_id:
            assert 5 == item_id
            flag.set()


def test_with_multiple_request_matcher():
    r = Request(Request.GET, '/books/1/pages/2')

    with is_set() as flag:
        with r / 'books':
            flag.set()

    with is_set() as flag:
        with r / 'books' / Integer as book_id:
            assert 1 == book_id
            flag.set()

    with is_set() as flag:
        with r / 'books' / Integer / 'pages' as book_id:
            assert 1 == book_id
            flag.set()

    with is_set() as flag:
        with r / 'books' / Integer / 'pages' / Integer as [book_id, page]:
            assert 1 == book_id
            assert 2 == page
            flag.set()

    with is_set() as flag:
        with r / 'books' / Integer / 'pages' / Integer / None as [book_id, page]:
            assert 1 == book_id
            assert 2 == page
            flag.set()


def test_for_request_matcher():
    r = Request(Request.GET, '/items/5')

    with is_set() as flag:
        for _ in r / 'items':
            flag.set()

    with is_set(False) as flag:
        for _ in r / 'books':
            flag.set()

    with is_set() as flag:
        for item_id in r / 'items' / Integer():
            assert 5 == item_id
            flag.set()

    with is_set() as flag:
        for item_id in r / 'items' / Integer():
            assert 5 == item_id
            flag.set()

    with is_set(False) as flag:
        for item_id in r / 'items' / None:
            assert 5 == item_id
            flag.set()

    with is_set() as flag:
        for book_id in r / 'items' / Integer / None:
            assert 5 == book_id
            flag.set()


def test_for_multiple_request_matcher():
    r = Request(Request.GET, '/books/1/pages/2')

    with is_set() as flag:
        for _ in r / 'books':
            flag.set()

    with is_set() as flag:
        for book_id in r / 'books' / Integer:
            assert 1 == book_id
            flag.set()

    with is_set() as flag:
        for book_id in r / 'books' / Integer / 'pages':
            assert 1 == book_id
            flag.set()

    with is_set() as flag:
        for book_id, page in r / 'books' / Integer / 'pages' / Integer:
            assert 1 == book_id
            assert 2 == page
            flag.set()

    with is_set() as flag:
        for book_id, page in r / 'books' / Integer / 'pages' / Integer / None:
            assert 1 == book_id
            assert 2 == page
            flag.set()
