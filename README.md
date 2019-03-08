### Pytcher

STILL A WORK IN PROGRESS

Pytcher is an HTTP routing DSL for Python. The main focus of Pytcher is to provide a human readable router syntax that supports complex path matching, parameter matching and header matching using nested routes.

To achieve this, we use a custom implementation of context manager (more info: https://stackoverflow.com/questions/12594148/skipping-execution-of-with-block/54765496#54765496) that makes a context manager skippable. This proposal has been rejected (https://www.python.org/dev/peps/pep-0377/)

This allows us to write an HTTP request router tree as follows:
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
