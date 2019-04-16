from pytcher.marshallers.json_marshaller import JSONMarshaller

marshaller = JSONMarshaller()


def test_json_mashaller_basic_types():
    assert '"test"' == marshaller.marshall('test')
    assert 'null' == marshaller.marshall(None)
    assert '5' == marshaller.marshall(5)
    assert '5.81' == marshaller.marshall(5.81)


def test_json_mashaller_list():
    assert '[]' == marshaller.marshall([])
    assert '["a1","b1","c1"]' == marshaller.marshall(['a1', 'b1', 'c1'])
    assert '[1,2,3]' == marshaller.marshall([1, 2, 3])
    assert '[null,null]' == marshaller.marshall([None, None])


def test_json_mashaller_dict():
    assert '{}' == marshaller.marshall({})
    assert '{"a1":"1","b1":"2","c1":"3"}' == marshaller.marshall({'a1': '1', 'b1': '2', 'c1': '3'})
    assert '{"a1":1,"b1":2,"c1":3}' == marshaller.marshall({'a1': 1, 'b1': 2, 'c1': 3})
