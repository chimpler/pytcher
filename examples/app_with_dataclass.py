# flake8: noqa: E999
import json
from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json

from pytcher import Request, Integer, AppRouter, Response


@dataclass_json
@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


class MyWebApp(AppRouter):
    def __init__(self):
        words = [
            'wine',
            'pizza',
            'cheese',
            'peanuts',
            'ice-cream'

        ]
        self._inventory = [
            InventoryItem(word, 10 + i, i + 1)
            for i in range(10)
            for word in words
        ]

    def serialize(self, root_obj, status_code: int, headers: Dict[str, str]):
        def to_dict(obj):
            if isinstance(obj, list):
                return [
                    to_dict(child)
                    for child in obj
                ]
            elif isinstance(obj, InventoryItem):
                return InventoryItem.schema().dump(obj)

        return Response(json.dumps(to_dict(root_obj)))

    def route(self, r: Request):
        with r.get / 'items':
            with r / Integer() as [item_index]:
                return self._inventory[item_index]

            with r.end:
                return self._inventory


if __name__ == '__main__':
    print()
    print('Try: curl localhost:8000/items')
    print('Try: curl localhost:8000/items/2')
    print()

    MyWebApp().start()
