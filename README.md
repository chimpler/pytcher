[![pypi](http://img.shields.io/pypi/v/pytcher.png)](https://pypi.python.org/pypi/pytcher)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/Pytcher.svg)](https://pypi.python.org/pypi/pytcher/)
[![Build Status](https://travis-ci.org/chimpler/pytcher.svg)](https://travis-ci.org/chimpler/pytcher)
[![Downloads](https://img.shields.io/pypi/dm/pytcher.svg)](https://pypistats.org/packages/pytcher)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/684cdd4d82734702ac612bf8b25fc5a0)](https://www.codacy.com/app/francois-dangngoc/pyhocon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chimpler/pyhocon&amp;utm_campaign=Badge_Grade)
[![License](https://img.shields.io/pypi/l/Pyhocon.svg)](https://pypi.python.org/pypi/pyhocon/)
[![Coverage Status](https://coveralls.io/repos/chimpler/pytcher/badge.svg)](https://coveralls.io/r/chimpler/pytcher)
[![Requirements Status](https://requires.io/github/chimpler/pytcher/requirements.svg?branch=master)](https://requires.io/github/chimpler/pytcher/requirements/?branch=master)
[![Join the chat at https://gitter.im/chimpler/pytcher](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/chimpler/pytcher?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

### Pytcher


Pytcher is an HTTP routing DSL for Python. The main focus of Pytcher is to provide a human readable router syntax that supports complex path matching, parameter matching and header matching using nested routes.
We also try to limit scope of variables not relying on global variables.
Pytcher will be mostly used to implement REST APIs and so sessions will not be supported.

Example of a simple CRUD REST server:
```python
from pytcher import App, Router, Request, Integer


class MyRouter(Router):
    def __init__(self):
        self.version = 'v1'
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    def route_handler(self, r: Request):
        with r / self.version / 'items':
            with r.end:
                with r.get:
                    return self._items

                with r.post:
                    self._items.append(r.json)
                    return self._items[-1]

            with r / Integer() as [item_id]:
                with r.get:
                    return self._items[item_id]

                with r.put:
                    self._items[item_id] = r.json
                    return self._items[item_id]

                with r.delete:
                    return self._items.pop(item_id)


app = App(MyRouter())


if __name__ == '__main__':
    app.start()
```

Start the app:

    $ python my_app.py
    
Or using uwsgi:

    # uwsgi --http :8000 --wsgi my_app:app

Optionally you can use the additional options:
`--pp` directory where it is located (e.g., `examples`)
`--wsgi-file` name of the file (e.g., `my_app.py`) 
`-H` <path to virtual environment> (e.g., `venv`)

Then, in another window you can run commands such as:

    $ curl localhost:8000/v1/items  # list all the items
    $ curl localhost:8000/v1/items/2  # get the second item
    $ curl localhost:8000/v1/items -XPOST -d'"beer"'  # add item "beer"
    $ curl localhost:8000/v1/items/0 -XPUT -d'"donut"'  # replace first item with donut
    $ curl localhost:8000/v1/items/2 -XDELETE  # delete second item

We can use contextmanager here `with` using a custom implementation ([more info](https://stackoverflow.com/questions/12594148/skipping-execution-of-with-block/54765496#54765496))
that makes a context manager skip the body of the `with` if a condition is not fulfilled.
This is known as [PEP-377](https://www.python.org/dev/peps/pep-0377/) which has been [rejected](https://www.python.org/dev/peps/pep-0377/).

We also offer another implementation that is using a `for` construct without using any hack.
Using with | Using for
------------|:------:
`with r / 'authors' / Integer() / 'books' / Integer()  as [author_id, book_id]:` | `for [author_id, book_id] in r / 'authors' / Integer() / 'books' / Integer()` 
`with r.get:` | `for _ in r.get`

For more examples, check out the [examples](https://github.com/chimpler/pytcher/tree/master/examples) directory.

# Compatibility

Python      | Compatible
------------|:------:
cpython 3   | :white_check_mark:
pypy 3      | :white_check_mark:

## TODO

Items                                     | Status
------------------------------------------| :-----:
Support AND (&)                           | :white_check_mark:
Support OR (\|)                           | :white_check_mark:
Support /                                 | :white_check_mark:
Support //                                | :x:
Support GET                               | :white_check_mark:
Support PUT                               | :white_check_mark:
Support POST                              | :white_check_mark:
Support PATCH                             | :white_check_mark:
Support parameter                         | :white_check_mark:
Support header                            | :white_check_mark:
Automatically generate route path for doc | :x:
WSGI                                      | :white_check_mark:
tests                                     | :x:
cookies                                   | :x:
docker                                    | :x:
middleware                                | :x:
plugin					                  | :x:
websocket			                	  | :x:
codec gzip                                | :x:
subroutes                                 | :white_check_mark:
marshallers (json, data class, namedtuple)|
