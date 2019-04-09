# Quickstart

First, make sure that you have Pytcher installed and up to date:

    $ pip install pytcher --upgrade
    
## Create a simple web service

Let's create a simple web service that returns `Hello World!`

```python
from pytcher import App, route

class MyRoute(object):
   @route
   def route(self, r): 
       return 'Hello World!'
     
route = MyRoute()
App(route).start()
```

You can run it as follows:

    $ python run_app.py
    
On another window:

    $ curl localhost:8080
    
    "Hello World!"
    
## Creating a more complex web service using a routing tree

Let's create a more complex CRUD service with the endpoints:
* `/items`
* `/items/<number>`

```python
from pytcher import App, Router, Request, Integer, route


class MyRouter(Router):
    def __init__(self):
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    @route
    def route(self, r: Request):
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

                with r.delete:
                    return self._items.pop(item_id)


if __name__ == '__main__':
    app = App(MyRouter())
    app.start()
``` 

## Create a simple web service using dataclasses

## Create a simple web service using annotation

For those more used to using decorators like in Flask, one can decorate multiple methods using a path and method.
One can also use multiple classes to do so and combine with the routing tree structure.



