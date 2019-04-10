Marshalling converts Python data (int, str, float, list, dict, data classes, named tuples) into a format that can be send across the wire.
The user can request a particular format to be returned using the `Accept` request HTTP header:

* `application/json`: accept JSON output
* `application/xml`: accept XML output
* `text/csv`: accept CSV output
* `*/*`: accept anything

## Default supported types

By default, pytcher accepts `application/json` and returns a JSON format output.

Out of the box, it can marshall the followings:

 Type         | Description  | Example               | Output
--------------|--------------|-----------------------|-------
`dict`        | dictionary   | `{'key': 'value'}`    | `{"key":"value}`
`list`        | list         | `['abc', 'cde']`      | `["abc","cde"]`
`namedtuple`  | named tuples | `Item('apple', 1.25)` | `{"name":"apple","price":1.25}`
`@dataclass`  | data class   | `Item('apple', 1.25)` | `{"name":"apple","price":1.25}`
`enum`        | enum         | `Color.RED`           | `"RED"`
`str`         | string       | `'apple'`             | `"apple"`
`int`         | integer      | `5`                   | `5`
`float`       | float        | `5.12`                | `5.12`
`date`        | date         | `datetime.date(2019, 2, 3)` | `2019-02-03`
`datetime`    | datetime (no timezone) | `datetime.datetime(2019, 2, 3, 12, 32, 1)` | `2019-02-03T12:32:01.000`
`datetime`    | datetime (with timezone) | `datetime.datetime(2019, 2, 3, 12, 32, 1, tzinfo=pytz.UTC)` | `2019-02-03T12:32:01.000+00:00`

A namedtuple can be defined as follows:
```python
from collections import namedtuple

Item = namedtuple('Item', ['name', 'price'])

apple = Item('apple', 1.25)
```

A dataclass can be defined as follows:
```python
from dataclasses import dataclass

@dataclass
class Item(object):
    name: str
    price: float
    
apple = Item('apple', 1.25)    

```

An enum can be defined as follows:
```python
from enum import Enum
class Color(Enum):
    RED = 1
    GREEN = 2

red = Color.RED
```

## Additional types

One can also add additional types to support as follows:
```python
TODO
```

## Adding new accept formats