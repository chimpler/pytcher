from collections import namedtuple
from dataclasses import dataclass

import pytest

from pytcher.marshallers.json_marshaller import JSONMarshaller

marshaller = JSONMarshaller()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ('test', '"test"'),
        (None, 'null'),
        (5, '5'),
        (5.81, '5.81'),
        (False, 'false'),
        (True, 'true'),
    ]
)
def test_json_mashaller_basic_types(test_input, expected):
    assert expected == marshaller.marshall(test_input)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ([], '[]'),
        (['a1', 'b1', 'c1'], '["a1","b1","c1"]'),
        ([1, 2, 3], '[1,2,3]'),
        ([None, None], '[null,null]')
    ]
)
def test_json_mashaller_list(test_input, expected):
    print(marshaller.marshall(test_input))
    assert expected == marshaller.marshall(test_input)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ({}, '{}'),
        ({'a1': '1', 'b1': '2', 'c1': '3'}, '{"a1":"1","b1":"2","c1":"3"}'),
        ({'a1': 1, 'b1': 2, 'c1': 3}, '{"a1":1,"b1":2,"c1":3}')
    ]
)
def test_json_mashaller_dict(test_input, expected):
    assert expected == marshaller.marshall(test_input)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ({'a': [], 'b': [1, 2, 3]}, '{"a":[],"b":[1,2,3]}'),
        ([{'a': 1}, {'b': 2}], '[{"a":1},{"b":2}]'),
        ({'a': [], 'b': [None, "abc", "xyz"]}, '{"a":[],"b":[null,"abc","xyz"]}'),
    ]
)
def test_json_mashaller_dict_list(test_input, expected):
    assert expected == marshaller.marshall(test_input)


Fruit = namedtuple('Item', ['name', 'price'])


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (Fruit('apple', 1), '{"name":"apple","price":1}'),
        (Fruit('pear', 1.25), '{"name":"pear","price":1.25}'),
        (Fruit('apple', None), '{"name":"apple","price":null}')
    ]
)
def test_json_marshaller_namedtuple(test_input, expected):
    assert expected == marshaller.marshall(test_input)


@dataclass
class Animal(object):
    name: str
    weight: float


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (Animal('cow', 1600), '{"name":"cow","weight":1600}'),
        (Animal('pig', 220), '{"name":"pig","weight":220}'),
        (Animal('chicken', 1.4), '{"name":"chicken","weight":1.4}'),
        (Animal('ghost', None), '{"name":"ghost","weight":null}')
    ]
)
def test_json_marshaller_dataclass(test_input, expected):
    assert expected == marshaller.marshall(test_input)
