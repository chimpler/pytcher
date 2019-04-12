# flake8: noqa: E999
from dataclasses import dataclass

from pytcher import Integer, Request, route
from pytcher.app import App


@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


class MyRouter(object):
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

    @route
    def route(self, r: Request):
        with r / 'items':
            with r / Integer() as [item_index]:
                with r.get:
                    return self._inventory[item_index]

                with r.put:
                    item = r.entity(InventoryItem)
                    self._inventory[item_index] = item
                    return item

                with r.delete:
                    item = self._inventory[item_index]
                    del self._inventory[item_index]
                    return item

            with r.end:
                with r.get:
                    return self._inventory

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
