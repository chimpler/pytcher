Pytcher is a REST micro-framework for Python 3 that relies on a routing tree
similar to [RODA](http://roda.jeremyevans.net/) in Ruby, [Akka HTTP](https://doc.akka.io/docs/akka-http/current/index.html) in Scala or [Javalin](https://javalin.io/) in Java.

!!! danger
    Under development

## Example of routing tree

```python
from pytcher import App, Router, Request, Integer, route


class MyRouter(Router):
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
  

## Features

- Routing tree definition
- Marshalling / Unmarshalling of `data classes` (using types), `namedtuples`, `date`, `datetime`, `uuid`, ...   
- Additional Routing decorators similar to Flask
- Well scoped objects (no global variables)
- Support for WSGI
