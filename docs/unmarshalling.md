It is common to read payload (in JSON) sent from the client using the `POST` or `PUT` method.
In most cases, the `POST` request will send the JSON representation of a Python object that will then
need to be unmarshalled to an object. This can be achieved using the `entity` method of the `Request` object passed to the function decorated with `@route`.

Supported types:

Type | Description | Example
-----|-------------|--------
`:::python int`  | integer     | `:::json 3`
`:::python float`| float       | `:::json 3.4`
`:::python str`  | string      | `:::json "test"`
`:::python boolean` | boolean  | `:::json "true"`
`:::python None` | NULL value   | `:::json NULL`
`:::python datetime` | datetime | `:::json "2019-02-01T02:03:04"`
`:::python datetime` with timezone | datetime with timezone | `:::json "2019-02-01T02:03:04-04:00"`
`:::python timezone` | timezone | `:::json "America/New_York"`
`:::python date` | date | `:::json "2019-04-02"`
`:::python time` | time | `:::json "14:03:12"`
data class | dataclass | dictionary representing the data class
`:::python list` | list | `:::json [1, 2, 3]`
`:::python dict` | dictionary | `:::json {"key": "value"}`
namedtuple | named tuple | dictionary representing the named tuple

!!! info
    To parse `datetime`, `date` and `time` we rely on the library [dateutil](https://dateutil.readthedocs.io/en/stable/) and
    for parsing `timezone`, we use the library [pytz](https://pythonhosted.org/pytz/).

## Example

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
`:::python r.entity(List[Float])` | Create a list of float
`:::python r.entity(MyDataClassObject)` | Create the data class object `Item`
`:::python r.entity(List[Item])` | Create a list of data classes `Item`
`:::python r.entity(Dict[Str, Item])` | Create a dictionary of `Str` -> `Item`

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