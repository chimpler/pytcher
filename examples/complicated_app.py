# flake8: noqa: E999
from pytcher import App, Router, Request, Integer
from pytcher.unmarshallers import Unmarshaller


class Person(object):
    def __init__(self, name):
        self.name = name

class AdminRouter(Router):
    def route(self, r: Request):
        person = r.entity(Person)

        with r / 'users':
            return ['darth', 'bear'] + [person.name]

        with r.end:
            return 'admin page'


class MyRouter(Router):
    def __init__(self):
        self._items = ['pizza', 'cheese', 'ice-cream', 'butter']

    def route(self, r: Request):
        with r / 'admin':
            return r.route(AdminRouter())

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

                with r.delete:
                    return self._items.pop(item_id)


class PersonUnmarshaller(Unmarshaller):
    def unmarshall(self, data):
        return Person(**data)


app = App(
    router=MyRouter(),
    unmarshallers={
        Person: PersonUnmarshaller()
    }
)


if __name__ == '__main__':
    app.start()
