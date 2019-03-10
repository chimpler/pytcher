# flake8: noqa: E999
import json
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from pytcher import App, Request, Integer


@dataclass_json
@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


class MyWebApp(object):
    def __init__(self):
        words = [
            'wine',
            'pizza',
            'cheese',
            'peanuts',
            'ice-cream'

        ]
        self._inventory = [
            InventoryItem(word, 10 + i, i)
            for i in range(10)
            for word in words
        ]

    def _output_serializer(self, root_obj):
        def serialize(obj):
            if isinstance(obj, list):
                return [
                    serialize(child)
                    for child in obj
                ]
            elif isinstance(obj, InventoryItem):
                return InventoryItem.schema().dump(obj)

        return json.dumps(serialize(root_obj))

    def _route_handler(self, r: Request):
        with r.get / 'items':
            with r / Integer() as [item_index]:
                return self._inventory[item_index]

            with r.end:
                return self._inventory


    def run(self):
        print()
        print('Try: curl curl localhost:8000/items')
        print('Try: curl curl localhost:8000/items/2')
        print()
        App().start(self._route_handler, output_serializer=self._output_serializer)


if __name__ == '__main__':
    MyWebApp().run()
