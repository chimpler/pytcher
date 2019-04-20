[![pypi](http://img.shields.io/pypi/v/pytcher.png)](https://pypi.python.org/pypi/pytcher)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/Pytcher.svg)](https://pypi.python.org/pypi/pytcher/)
[![Build Status](https://travis-ci.org/chimpler/pytcher.svg)](https://travis-ci.org/chimpler/pytcher)
[![Downloads](https://img.shields.io/pypi/dm/pytcher.svg)](https://pypistats.org/packages/pytcher)
[![Coverage Status](https://coveralls.io/repos/github/chimpler/pytcher/badge.svg?branch=master)](https://coveralls.io/github/chimpler/pytcher?branch=master)
[![License](https://img.shields.io/pypi/l/Pyhocon.svg)](https://pypi.python.org/pypi/pyhocon/)
[![Requirements Status](https://requires.io/github/chimpler/pytcher/requirements.svg?branch=master)](https://requires.io/github/chimpler/pytcher/requirements/?branch=master)

```

WORK IN PROGRESS

```

### Pytcher

Pytcher is an HTTP routing DSL for Python. The main focus of Pytcher is to provide a human readable router syntax that supports complex path matching, parameter matching and header matching using nested routes.

### Features
* Routing tree definition using `with` or `for` construction
* Marshalling of Python objects (data classes, namedtuples, date, datetime, uuid, ...) that supports custom encoders
* Unmarshalling of JSON to Python objects (data classes, namedtuples, date, datetime, uuid, ...) supporting `typing` (e.g., `Dict[str, MyDataClass]`) syntax and custom decoders. 
* Additional Routing decorators similar to Flask
* Well scoped objects (no global variables)
* Support for WSGI

The routing tree can be defined as follows:
```python
from pytcher import App, Request, Integer, route


class MyRouter(object):
    def __init__(self):
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    @route
    def route(self, r: Request):
        with r / 'items':  # if URL starts with /items
            with r.end:  # if there is nothing after /items
                with r.get:  # If it's a get request
                    return self._items

                with r.post:  # If request is a post request
                    self._items.append(r.json)
                    return self._items[-1]

            with r / Integer() as item_id:  # If the URL is /items/<integer> then bind item_id to the integer
                with r.get:  # If the request is a get request
                    return self._items[item_id]

                with r.put:  # If the request is a put request
                    self._items[item_id] = r.json
                    return self._items[item_id]

                with r.delete:  # If the request is a delete request
                    return self._items.pop(item_id)


if __name__ == '__main__':
    app = App(MyRouter())
    app.start()
```

