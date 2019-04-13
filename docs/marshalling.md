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
`:::python dict`        | dictionary   | `:::python {'key': 'value'}`    | `:::json {"key":"value}`
`:::python list`        | list         | `:::python ['abc', 'cde']`      | `:::json ["abc","cde"]`
`:::python namedtuple`  | named tuples | `:::python Item('apple', 1.25)` | `:::json {"name":"apple","price":1.25}`
`:::python @dataclass`  | data class   | `:::python Item('apple', 1.25)` | `:::json {"name":"apple","price":1.25}`
`:::python enum`        | enum         | `:::python Color.RED`           | `:::json "RED"`
`:::python str`         | string       | `:::python 'apple'`             | `:::json "apple"`
`:::python int`         | integer      | `:::python 5`                   | `:::json 5`
`:::python float`       | float        | `:::python 5.12`                | `:::json 5.12`
`:::python date`        | date         | `:::python datetime.date(2019, 2, 3)` | `:::json "2019-02-03"`
`:::python datetime`    | datetime (no timezone) | `:::python datetime.datetime(2019, 2, 3, 12, 32, 1)` | `:::json "2019-02-03T12:32:01.000"`
`:::python datetime`    | datetime (with timezone) | `:::python datetime.datetime(2019, 2, 3, 12, 32, 1, tzinfo=pytz.UTC)` | `:::json "2019-02-03T12:32:01.000+00:00"`

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