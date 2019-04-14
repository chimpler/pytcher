# flake8: noqa: E999
import logging
from dataclasses import dataclass

from pytcher import Request, route, Integer
from pytcher.app import App

logger = logging.getLogger(__name__)


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

    @route(prefix='/items')
    def handle_items(self, r: Request):
        with r / Integer as [item_index]:
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')

    app = App(MyRouter(), debug=True)
    print()
    print('Try: curl localhost:8000/items')
    print('Try: curl localhost:8000/items/2')
    print()

    app.start()
