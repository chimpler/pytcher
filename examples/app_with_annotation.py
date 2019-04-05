# flake8: noqa: E999
from dataclasses import dataclass

from pytcher import Integer, Request, route
from pytcher.app import App


@dataclass
class InventoryItem(object):
    name: str
    unit_price: float
    quantity: int = 0


@route(path='/')
def test():
    return []


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
    def get_item(self, request, id):
        return self._inventory[id]

    @route(path='/items', method='GET')
    def list_items(self, request):
        return self._inventory

    def route(self, r: Request):
        with r / 'items':
            with r.get / Integer() as [item_index]:
                return self._inventory[item_index]

            with r.end:
                with r.get:
                    return self._inventory

                with r.post:
                    item = r.entity(InventoryItem)
                    self._inventory.append(item)
                    return item


if __name__ == '__main__':
    app = App(MyRouter())
    print()
    print('Try: curl localhost:8000/items')
    print('Try: curl localhost:8000/items/2')
    print()

    app.start()
