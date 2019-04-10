It is common to read payload (in JSON) sent from the client using the `POST` or `PUT` method.
In most cases, the `POST` request will send the JSON representation of a Python object that will then
need to be unmarshalled to an object. This can be achieved using the `entity` method of the `Request` object passed to the function decorated with `@route`.

For example:

We consider Item to be a data class defined as follows:
```python
from dataclasses import dataclass

@dataclass
class Item(object):
    name: str
    price: float
    
apple = Item('apple', 1.25)
```

Example | Description
--------|------------
r.entity(List[Float]) | Create a list of float
r.entity(MyDataClassObject) | Create the data class object `Item`
r.entity(List[Item]) | Create a list of data classes `Item`
r.entity(Dict[Str, Item]) | Create a dictionary of `Str` -> `Item`

Optionally, one can specify a [JSON path](https://github.com/h2non/jsonpath-ng). For example if the `Item` is wrapped in a `"data"` element:
```json
{
  "data": {
    "name": "pear",
    "price": 1.45
  }
}
```

Item can be obtained using the json path `$.data` as follows:
```python
r.entity(Item, '$.data')
```