from pytcher import Request, Integer


def test_request():
    request = Request(Request.GET, '/items/5')
    assert (request / 'items')._is_match
    assert not (request / 'books')._is_match
    assert (request / 'items' / Integer())._is_match
    assert (request / 'items' / Integer)._is_match
