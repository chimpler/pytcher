Routes can be defined using different ways:

* using the decorator `@route`
* within a function/method decorated using `@route` and using the `with` statement
* within a function/method decorated using `@route` and using the `for` statement

## @route decorator

One can use the `:::python @route` decorator on a function or a class method which has
as parameter a request object.

For instance:
```python
from pytcher import App, Request, route

@route
def route(request: Request):
    return 'Hello world'
    
app = App([route])
app.run()
```

Also, like Flask, one can also pass the expected HTTP method (default to `GET`) and the
path (that can contain binding variables) that defaults to `/`.

In this case, the parameters of the function/method will be:

* request object
* binding variables  

For instance:
```python
from pytcher import App, Request, route

@route(path='/items/<int:item_id>', method='GET')
def route(request: Request, item_id: int):
    return {
        'item': item_id
    }

```

## Routing tree

Inside a function or a method decorated with `:::python @route`
The routing tree can be defined using `:::python with` statements or `:::python for` loops.

The following example using `:::python with` statements:

```python
from pytcher import route, Request, Integer

@route
def route(r: Request):
    with r / 'v1':
        with r.get / 'items' / Integer as item_id:
            return {
                'Item': item_id
            }    
```

Can be rewritten with `:::python for` loops as follows:

```python
from pytcher import route, Request, Integer

@route
def route(r: Request):
    for _ in  r / 'v1':
        for item_id in r.get / 'items' / Integer:
            return {
                'Item': item_id
            }    
```

Let's consider an example with 2 bindings. In this case, the binding will return a list instead of a single value.
For example, the URL path `/books/2/pages/3` will match the route `:::python r / 'books' / Integer / 'pages' / Integer` and binds
the 2 `int` to a list of 2 elements:
```python
with r / 'books' / Integer / 'pages' / Integer as [book_id, page]:
    return {
        'book_id': book_id,
        'page': page
    }
```

or using a `for` loop construction:
```python
for book_id, page in  r / 'books' / Integer / 'pages' / Integer:
    return {
        'book_id': book_id,
        'page': page
    }
```

### Method matcher

The HTTP methods can be matched as follows:

Method | route
-------|--------
`GET`    | `:::python with r.get:`
`PUT`    | `:::python with r.put:`
`POST`    | `:::python with r.post:`
`DELETE`    | `:::python with r.delete:`
`PATCH`    | `:::python with r.patch:`
`HEAD`    | `:::python with r.head:`

### Path matcher

Paths can be defined using path elements separated by `/`.
For example `:::python with r / 'v2' / 'items:'` will match the path `/v2/items`.

One can also use the following matchers:

Matcher | Description | Example
--------|-------------|--------- 
`:::python Integer(min=None, max=None)` | Match an Integer between `min` and `max` | `:::python with r / 'books' / Integer() / 'pages' / Integer() as [book_id, page]:`   
`:::python Float(min=None, max=None)` | Match a float between `min` and `max` | `:::python with r / 'values' / Float() as [price]:`
`:::python Date(format='YYYY-MM-DD')` | Match a date | `:::python with r / 'data' / Date() as [date]:`
`:::python Choice(value1, value2, ..., ignore_case=True])` | Match different strings | `:::python with r / Choice(['books', 'novels]) as [book_type]:`   
`:::python str` | Match a string | `:::python with r / 'data':`
`:::python Regex(regex, flags, data_types)` | Match a regex | `:::python with r / 'data' / Regex('(.*)-(.*)') as [[a, b]]:`
`:::python None` | Match the end of the path | `:::python with r / 'items' / None:`
`:::python request.end` | match the end of the path | `:::python with r.end:`

!!! Info
    If you use default parameters, you can use the matcher class or the instance. For example `Integer` or `Integer()`

#### Integer matcher
`:::python Integer(min: int = None, max: int = None)`: Matches if the path element is an integer. Optionally you can provide the boundaries (inclusive).

#### Float matcher
`:::python Float(min: float = None, max: float = None)`: Matches if the path element is a float. Optionally you can provide the boundaries (inclusive).

#### Date matcher
`:::python Date(format='%Y-%m-%d')`: Matches if the path element is a date. By default the format is `%Y-%m-%d` (e.g., `2019-03-02`). For the format see the [Python datetime page](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior). 

#### Choice matcher
`:::python Choice(choice1: str, choice2: str, ..., ignore_case: bool = True)`: Matches if the path element is one of strings provided. By default it is case insensitive but one can set `ignore_case` to `False` to be case sensitive.
#### str matcher

`:::python str`: Simply use a string for exact match, for example `r / 'items'` will match if the path element matches `items`

`:::python None`: Indicate the end of the request URL. For example `r / 'items' / None` indicates that the URL ended at `items`

`:::python end`: Indicate the end of the request URL. For example `r.end` indicates that the URL ended

#### Regex matcher
If no matching group is provided to the Regex matcher, it will return the whole string that matches.
If a single capturing group is provided, it will return the string that matches the group
If multiple capturing groups are provided, it will return an array of strings that matches the groups.

It can also take care of type conversion by providing data_types which is an array of types the groups are supposed to be.
For example:
```python
with r / Regex('^fruit-(?P<name>.*)-(?P<size>\d+)$', data_types=[str, int]) as [name, size]:
    return {
        'fruit': name,
        'size': size
    }
``` 

will bind the first group as a `str` and size as an `int`. The URL `/fruit-orange-15` will result in the following result:
```json
{
  "fruit": "orange",
  "size": 15
}
```

#### None matcher

#### Example using path matchers

Here is an example of routing tree:
```python
from pytcher import route, Request

@route
def route(r: Request):
    with r / 'books':  # If path starts with '/books'
        with r.end:  # If path matches exactly `/books`
            return {"message": "something"}
            
        with r / 'info' / None:  # If path matches exactly `/books/info`:
            return {"info": "nothing"}
            
        with r / String() / 'page' / Integer() / None as [book_id, page]:  # For example /books/test/page/10
            return {
                "book": book_id,
                "page": page
            }
```

### Parameter matcher

Conditions can be put on parameter values (for example `http://localhost/items?token=45ab`). 

This can be done as follows:
```python
from pytcher import route, Request

@route
def route(r: Request):
    with r.p['token'] == '45ab':
        return {
            'message': 'Hello!'
        }
     
    return {
        'message': "Bye!"
    }
```

It can also use operators such as `>` or `<` for numeric values.

Below is the full list of supported operators:

Operator | Description | Example
---------|-------------|--------
`==`       | equal       | `:::python r.p['token'] == 'secret-token'` 
`!=`       | not equal   | `:::python r.p['type'] != 'fruit'` 
`>`       | greater than       | `:::python r.p['price'] > 100` 
`<`       | less than       | `:::python r.p['price'] < 100` 
`>=`       | greater or equal       | `:::python r.p['price'] >= 100` 
`<=`       | less or equal       | `:::python r.p['price'] <= 100`
`in`       | contains     | `:::python 'apple' in r.p['fruits']`

### Header matcher

!!! info
    HTTP Headers are not case-sensitive (so `X-Organization` will be treated the same as `x-organization`)

Similarly to parameter matchers, conditions can be put on header values. For example one can check if `X-Organization` is set to `my-company`.
This can be done as follows:
```python
from pytcher import route, Request

@route
def route(r: Request):
    with r.h['X-Organization'] == 'my-company':
        return {
            'message': 'Hello my-company employee!'
        }
     
    return {
        'message': "Go away!"
    }

```

It can also use operators such as `>` or `<` for numeric values.

Below is the full list of supported operators:

Operator | Description | Example
---------|-------------|--------
`==`       | equal       | `:::python r.h['Token'] == 'secret-token'` 
`!=`       | not equal   | `:::python r.h['X-Organization'] != 'my-company'` 
`>`       | greater than       | `:::python r.h['money'] > 100` 
`<`       | less than       | `:::python r.h['money'] < 100` 
`>=`       | greater or equal       | `:::python r.h['money'] >= 100` 
`<=`       | less or equal       | `:::python r.h['money'] <= 100`
`in`       | contains     | `:::python 'apple' in r.h['fruits']`

### Combining matchers

One can use boolean expressions with `&` (and) and `|` (or).
For example:
```python
from pytcher import route, Request

@route
def route(r: Request):
    with (r / 'items') & r.h['X-Organization'] == 'my-company':
        return {
            "items": [
                {"name": "pear"},
                {"name": "apple"}
            ]
        }
```
