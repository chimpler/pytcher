# flake8: noqa: E999
from pytcher import App, Request, Integer


class MyApp(object):
    def __init__(self):
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    def route_handler(self, r: Request):
        with r / 'items':
            with r.end:
                with r.get:
                    return self._items

                with r.post:
                    self._items.append(r.json)
                    return self._items[-1]

            with r / Integer() as [item_id]:
                with r.get:
                    return self._items[item_id]

                with r.put:
                    self._items[item_id] = r.json
                    return self._items[item_id]

    def run(self):
        App().start(route_handler=self.route_handler)


if __name__ == '__main__':
    MyApp().run()
