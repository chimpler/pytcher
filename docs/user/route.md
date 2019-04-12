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
@route
def route(r: Request)
    with r / 'v1':
        with r.get / 'items' / Integer as [item_id]:
            return {
                'Item': item_id
            }    
```

Can be rewritten with `:::python for` loops as follows:

```python
@route
def route(r: Request)
    for _ in  r / 'v1':
        for item_id in r.get / 'items' / Integer:
            return {
                'Item': item_id
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
`:::python Regex()` | Match a regex | `:::python with r / 'data' / Regex('(.*)-(.*)') as [[a, b]]:`
   

### Parameter matcher

Conditions can be put on parameter values (for example `http://localhost/items?token=45ab`). 

This can be done as follows:
```python
with r.p['token] == '45ab':
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
with (r / 'items') & r.h['X-Organization'] == 'my-company':
    return {
        "items": [
            {"name": "pear"},
            {"name": "apple"}
        ]
    }
```
