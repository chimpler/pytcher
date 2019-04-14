Pytcher is a REST micro-framework for Python 3 that relies on a routing tree
similar to [RODA](http://roda.jeremyevans.net/) in Ruby, [Akka HTTP](https://doc.akka.io/docs/akka-http/current/index.html) in Scala or [Javalin](https://javalin.io/) in Java.

!!! danger
    Under development

## Features

- Marshalling / Unmarshalling of `data classes` (using types), `namedtuples`, `date`, `datetime`, `uuid`, ...   
- Routing tree definition
- Additional Routing decorators similar to Flask
- Well scoped objects (no global variables)
- Support for WSGI

# Getting started

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

["pizza","cucumber","ice-cream","butter", "ham"]
```

``` tab="DELETE /items/1"
$ curl localhost:8000/items/1 -XDELETE

"cucumber"

$ curl localhost:8000/items

["pizza","ice-cream","butter", "ham"]
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

In this example, we will take advantage of the [data classes](https://docs.python.org/3/library/dataclasses.html) that were introduced in Python 3.7.

```python
from dataclasses import dataclass

from pytcher import Integer, Request, route
from pytcher.app import App


@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


class MyRouter(object):
    def __init__(self):
        words = [
            'wine',
            'pizza',
            'cheese',
            'peanuts',
            'ice-cream'

        ]
        self._inventory = [
            InventoryItem(word, 10 + i, i + 1)
            for i in range(10)
            for word in words
        ]

    @route
    def route(self, r: Request):
        with r / 'items':
            with r / Integer() as [item_index]:
                with r.get:
                    return self._inventory[item_index]

                with r.put:
                    item = r.entity(InventoryItem)
                    self._inventory[item_index] = item
                    return item

                with r.delete:
                    item = self._inventory[item_index]
                    del self._inventory[item_index]
                    return item

            with r.end:
                with r.get:
                    return self._inventory

                with r.post:
                    item = r.entity(InventoryItem)
                    self._inventory.append(item)
                    return item



if __name__ == '__main__':
    app = App(MyRouter())
    app.start()
```

On another window, try the following commands:

``` tab="GET /items"
$ curl localhost:8000/items

[
  {
    "name": "wine",
    "unit_price": 10,
    "quantity": 1
  },
  {
    "name": "pizza",
    "unit_price": 10,
    "quantity": 1
  },
  {
    "name": "cheese",
    "unit_price": 10,
    "quantity": 1
  },
  [...]
]  
```

``` tab="GET /items/1"
$ curl localhost:8000/items/1

{
  "name": "pizza",
  "unit_price": 10,
  "quantity": 1
}
```

``` tab="POST /items"
$ curl localhost:8000/items -H "Content-Type: application/json" -XPOST -d '{
  "name": "pizza",
  "unit_price": 10,
  "quantity": 1
}'

{
  "name": "pizza",
  "unit_price": 10,
  "quantity": 1
}
```

``` tab="PUT /items/1"
$ curl localhost:8000/items/1  -H "Content-Type: application/json" -XPUT -d '{
  "name": "corn",
  "unit_price": 1,
  "quantity": 2
}'

{
  "name": "corn",
  "unit_price": 1,
  "quantity": 2
}
```

``` tab="DELETE /items/1"
$ curl localhost:8000/items/1 -XDELETE

{
  "name": "pizza",
  "unit_price": 10,
  "quantity": 1
}
```

## Create a simple web service using annotation

For those more used to using decorators like in Flask, one can decorate multiple methods using a path and method.

```python
import logging
from dataclasses import dataclass

from pytcher import Request, route
from pytcher.app import App

logger = logging.getLogger(__name__)


@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


class MyRouter(object):

    def __init__(self):
        words = [
            'wine',
            'pizza',
            'cheese',
            'peanuts',
            'ice-cream'

        ]
        self._inventory = [
            InventoryItem(word, 10 + i, i + 1)
            for i in range(10)
            for word in words
        ]

    @route(path='/items/<int:id>', method='GET')
    def get_item(self, r: Request, id):
        return self._inventory[id]

    @route(path='/items', method='GET')
    def list_items(self, request):
        return self._inventory

    @route(path='/items', method='POST')
    def route(self, r: Request):
        with r.post:
            item = r.entity(InventoryItem)
            self._inventory.append(item)
            return item


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')

    app = App(MyRouter(), debug=True)
    app.start()

```

## Combining @route and routing tree

In this example, we combine the use of the `@route` decorator using the prefix `/items` with a routing tree.
This can be a common pattern, especially when using multiple router classes (e.g., one class with `/admin` and another one to handle `items`).

```python
import logging
from dataclasses import dataclass

from pytcher import Request, route, Integer
from pytcher.app import App

logger = logging.getLogger(__name__)


@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


class MyRouter(object):

    def __init__(self):
        words = [
            'wine',
            'pizza',
            'cheese',
            'peanuts',
            'ice-cream'
        ]

        self._inventory = [
            InventoryItem(word, 10 + i, i + 1)
            for i in range(10)
            for word in words
        ]

    @route(prefix='/items')
    def handle_items(self, r: Request):
        with r / Integer as [item_index]:
            with r.get:
                return self._inventory[item_index]

            with r.put:
                item = r.entity(InventoryItem)
                self._inventory[item_index] = item
                return item

            with r.delete:
                item = self._inventory[item_index]
                del self._inventory[item_index]
                return item

        with r.end:
            with r.get:
                return self._inventory

            with r.post:
                item = r.entity(InventoryItem)
                self._inventory.append(item)
                return item


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')

    app = App(MyRouter(), debug=True)
    print()
    print('Try: curl localhost:8000/items')
    print('Try: curl localhost:8000/items/2')
    print()

    app.start()
```

All the examples can be found in the [examples folder](https://github.com/chimpler/pytcher/tree/master/examples).

## More features

To use multiple routers, one can simply pass them to `App`. For example:
```python
app = App([AdminRouter(), ItemRouter()])
app.run()
```