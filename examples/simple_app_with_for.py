# flake8: noqa: E999
from pytcher import AppRouter, Request, Integer
from pytcher.app import App


class MyAppRouter(AppRouter):
    def __init__(self):
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    def route(self, r: Request):
        for _ in r / 'items':
            for _ in r.end:
                for _ in r.get:
                    return self._items

                for _ in r.post:
                    self._items.append(r.json)
                    return self._items[-1]

            for [item_id] in r / Integer():
                for _ in r.get:
                    return self._items[item_id]

                for _ in r.put:
                    self._items[item_id] = r.json
                    return self._items[item_id]

                for _ in r.delete:
                    return self._items.pop(item_id)


app = App(MyAppRouter())


if __name__ == '__main__':
    app.start()
