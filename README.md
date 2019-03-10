[![pypi](http://img.shields.io/pypi/v/pytcher.png)](https://pypi.python.org/pypi/pytcher)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/Pytcher.svg)](https://pypi.python.org/pypi/pytcher/)
[![Build Status](https://travis-ci.org/chimpler/pytcher.svg)](https://travis-ci.org/chimpler/pytcher)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/684cdd4d82734702ac612bf8b25fc5a0)](https://www.codacy.com/app/francois-dangngoc/pyhocon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chimpler/pyhocon&amp;utm_campaign=Badge_Grade)
[![License](https://img.shields.io/pypi/l/Pyhocon.svg)](https://pypi.python.org/pypi/pyhocon/)
[![Coverage Status](https://coveralls.io/repos/chimpler/pytcher/badge.svg)](https://coveralls.io/r/chimpler/pytcher)
[![Requirements Status](https://requires.io/github/chimpler/pytcher/requirements.svg?branch=master)](https://requires.io/github/chimpler/pytcher/requirements/?branch=master)
[![Join the chat at https://gitter.im/chimpler/pytcher](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/chimpler/pytcher?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

### Pytcher



Pytcher is an HTTP routing DSL for Python. The main focus of Pytcher is to provide a human readable router syntax that supports complex path matching, parameter matching and header matching using nested routes.

For example:
```python
from pytcher import App, Request, Integer


class MyApp(object):
    def __init__(self):
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    def route_handler(self, r: Request):
        with r / 'items':
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

    def run(self):
        App().start(route_handler=self.route_handler)


if __name__ == '__main__':
    MyApp().run()
```

This is achieved by using custom implementation of context manager ([more info](https://stackoverflow.com/questions/12594148/skipping-execution-of-with-block/54765496#54765496))
that makes a context manager skip the body of the `with` if a condition is not fulfilled.
This is known as [PEP-377](https://www.python.org/dev/peps/pep-0377/) which has been [rejected](https://www.python.org/dev/peps/pep-0377/).

For more examples, check out the [examples](https://github.com/chimpler/pytcher/tree/master/examples) directory.

We also offer another implementation that is using a `for` construct without using any hack.
In this case instead of writing:
```python
    with r / Integer() as [item_id]:
```

one can write:
```python
    for [item_id] in r / Integer():
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
