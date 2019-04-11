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
        with r / 'items':  # if URL starts with /items
            with r.end:  # if there is nothing after /items
                with r.get:  # If it's a get request
                    return self._items

                with r.post:  # If request is a post request
                    self._items.append(r.json)
                    return self._items[-1]

            with r / Integer() as [item_id]:  # If the URL is /items/<integer> then bind item_id to the integer
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

As you notice, we use the `with` statement context. In this case, if the request matches the condition (e.g., starts with `/items` or is `GET` request), then the code inside the block is executed. This can also be achieved using a `for` loop instead.

For example:

| using `with` |               using `for`                       |
| ----------- | ------------------------------------------------- |
| `:::py with r / 'items':`  | `:::py for _ in r / 'items':`          |
| `:::py with r.get / 'items' / Integer() as [item_id]:`  | `:::py for item_id in r.get / 'items' / 'Integer':` |


## Create a simple web service using dataclasses

## Create a simple web service using annotation

For those more used to using decorators like in Flask, one can decorate multiple methods using a path and method.
One can also use multiple classes to do so and combine with the routing tree structure.

