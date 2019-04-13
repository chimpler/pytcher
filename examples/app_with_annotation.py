# flake8: noqa: E999
import logging
from dataclasses import dataclass

from pytcher import Request, route
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

    @route(path='/items/<int:id>', method='GET')
    def get_item(self, r: Request, id):
        return self._inventory[id]

    @route(path='/items', method='GET')
    def list_items(self, request):
        return self._inventory

    @route(path='/items', method='POST')
    def route(self, r: Request):
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