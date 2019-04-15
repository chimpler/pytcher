import pytest

from pytcher import Integer, Request
from tests.utils import is_set


def test_raw_request_matcher():
    request = Request(Request.GET, '/items/5')
    assert (request / 'items').is_match is True
    assert not (request / 'books').is_match is True
    assert (request / 'items' / Integer()).is_match is True
    assert (request / 'items' / Integer).is_match is True
    assert (request / 'items' / Integer / None).is_match is True


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

    with is_set() as flag:
        with r / 'items' / Integer / None as item_id:
            assert 5 == item_id
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

    with is_set() as flag:
        for book_id in r / 'items' / Integer / None:
            assert 5 == book_id
            flag.set()
