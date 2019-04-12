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
    * `GET`: return the list of items
    * `POST`: add an item
* `/items/<number>`
    * `PUT`: replace the item at position `<number>`
    * `DELETE`: delete the item at position `<number>`

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

On another window, try the following commands:

``` tab="GET /items"
$ curl localhost:8000/items

["pizza","cheese","ice-cream","butter"]
```

``` tab="GET /items/1"
$ curl localhost:8000/items/1

"cheese"
```

``` tab="POST /items"
$ curl localhost:8000/items -XPOST -d "ham"

"ham"

$ curl localhost:8000/items

["pizza","cheese","ice-cream","butter", "ham"]
```

``` tab="PUT /items/1"
$ curl localhost:8000/items/1 -XPUT -d "cucumber"

"cucumber"

$ curl localhost:8000/items

["cucumber","cheese","ice-cream","butter", "ham"]
```

``` tab="DELETE /items/1"
$ curl localhost:8000/items/1 -XDELETE

"cucumber"

$ curl localhost:8000/items

["cheese","ice-cream","butter", "ham"]
```
    
As you notice, we use the `with` statement context. In this case, if the request matches the condition (e.g., starts with `/items` or is `GET` request), then the code inside the block is executed. 
This can also be achieved using a `for` loop instead.

For example:

| using `with` |               using `for`                       |
| ----------- | ------------------------------------------------- |
| `:::py with r / 'items':`  | `:::py for _ in r / 'items':`          |
| `:::py with r.get / 'items' / Integer() as [item_id]:`  | `:::py for item_id in r.get / 'items' / 'Integer':` |

!!! Info
    The author of Python did not approve requests to use `:::python with` statements to be conditional (i.e., execute the block
    if a certain condition occurs). We implemented it to make it work on cpython and possibly other implementations of Python.
    However using the `:::python for` loop construction is perfectly fine and does not violate the Python standard.

## Create a simple web service using dataclasses

## Create a simple web service using annotation

For those more used to using decorators like in Flask, one can decorate multiple methods using a path and method.
One can also use multiple classes to do so and combine with the routing tree structure.

