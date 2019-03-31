# flake8: noqa: E999
from dataclasses import dataclass
from datetime import timedelta

from pytcher import Integer, Request, Router
from pytcher.app import App


@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


class MyRouter(Router):
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

    def route(self, r: Request):
        with r / 'items':
            with r.get / Integer() as [item_index]:
                return self._inventory[item_index]

            with r.end:
                with r.get:
                    return [self._inventory, timedelta(1, 3893, 1000, 122)]

                with r.post:
                    item = r.entity(InventoryItem)
                    self._inventory.append(item)
                    return item


app = App(MyRouter())

if __name__ == '__main__':
    print()
    print('Try: curl localhost:8000/items')
    print('Try: curl localhost:8000/items/2')
    print()

    app.start()
