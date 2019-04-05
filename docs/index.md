# Welcome to Pytcher

Pytcher is a REST micro-framework for Python that relies on a routing tree
similar to RODA in Ruby, Akka HTTP in Scala or Javalin in Java.

## Features

- Marshalling / Unmarshalling of `data classes` (using types), `namedtuples`, `date`, `datetime`, `uuid`, ...   
- Routing tree definition
- Routing decorator similar to Flask
- Well scoped objects (no global variables)
- Support for WSGI

## Simple example
```python
from pytcher import App, Router, Request, Integer


class MyRouter(object):
    def __init__(self):
        self.version = 'v1'
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    @route
    def route(self, r: Request):
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

if __name__ == '__main__':
    app = App(MyRouter())
    app.start()
```
