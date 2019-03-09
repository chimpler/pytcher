### Pytcher



Pytcher is an HTTP routing DSL for Python. The main focus of Pytcher is to provide a human readable router syntax that supports complex path matching, parameter matching and header matching using nested routes.

For example:
```python
from pytcher import App, Request, Integer, Regex
import http

def route_handler(r: Request):
    with r / 'books' / Regex('c.*r') as [book_id]:
        with r.get | r.put:
            with r.h.has('X-Organization-Id'):
                return {'book': {'id': book_id}}

            return {'message': 'restricted access'}

        with r.post:
            return {'books': [{'id': 2}]}

    with (r.get / 'novels' / Integer() / 'authors' / Integer()) & (r.p['g'] == 3) as [novel_id, author_id]:
        return {'novel': novel_id, 'author': author_id, 'g': r.p['g'].int}


if __name__ == '__main__':
    App().start(route_handler)
```

This is achieved by using custom implementation of context manager ([more info](https://stackoverflow.com/questions/12594148/skipping-execution-of-with-block/54765496#54765496)) that makes a context manager skippable.
This is known as [PEP-377](https://www.python.org/dev/peps/pep-0377/) which has been [rejected](https://www.python.org/dev/peps/pep-0377/).

We also offer another implementation that is not using any hack:
```python
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
```

# Compatibility

Python      | Compatible
------------|:------:
cpython 3   | :white_check_mark:
pypy 3      | :white_check_mark:

## TODO

Items                                     | Status
------------------------------------------| :-----:
Support AND (&)                           | :white_check_mark:
Support OR (|)                            | :white_check_mark:
Support /                                 | :white_check_mark:
Support //                                | :x:
Support GET                               | :white_check_mark:
Support PUT                               | :white_check_mark:
Support POST                              | :white_check_mark:
Support PATCH                             | :white_check_mark:
Support parameter                         | :white_check_mark:
Support header                            | :white_check_mark:
Automatically generate route path for doc | :x:
WSGI                                      | :x:
tests                                     | :x:
