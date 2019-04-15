# Getting started

First, make sure that you have Pytcher installed and up to date:

    $ pip install pytcher --upgrade
    
## Create a simple web service

Let's create a simple web service that returns `Hello World!`

```python
from pytcher import App, Request, route

class MyRoute(object):
   @route
   def route(self, r: Request): 
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
{!examples/simple_app.py!}
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
| `:::py with r.get / 'items' / Integer() as item_id:`  | `:::py for item_id in r.get / 'items' / 'Integer':` |

!!! Info
    The author of Python did not approve requests to use `:::python with` statements to be conditional (i.e., execute the block
    if a certain condition occurs). We implemented it to make it work on cpython and possibly other implementations of Python.
    However using the `:::python for` loop construction is perfectly fine and does not violate the Python standard.

## Create a simple web service using dataclasses

In this example, we will take advantage of the [data classes](https://docs.python.org/3/library/dataclasses.html) that were introduced in Python 3.7.

```python
{!examples/app_with_dataclass.py!}
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
{!examples/app_with_annotation.py!}
```

## Combining @route and routing tree

In this example, we combine the use of the `@route` decorator using the prefix `/items` with a routing tree.
This can be a common pattern, especially when using multiple router classes (e.g., one class with `/admin` and another one to handle `items`).

```python
{!examples/app_with_annotation_and_routing_tree.py!}
```

## More features

To use multiple routers, one can simply pass them to `App`. For example:
```python
app = App([AdminRouter(), ItemRouter()])
app.run()
```