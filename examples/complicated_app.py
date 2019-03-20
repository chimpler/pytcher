# flake8: noqa: E999
import json
from dataclasses import dataclass


import dataclasses
from datetime import datetime
from json import JSONEncoder, JSONDecoder
from json.decoder import WHITESPACE

from pytcher import App, Router, Request, Integer, String
from pytcher.unmarshallers import Unmarshaller
from datetime import datetime
from typing import List
from pydantic import BaseModel


@dataclass
class Animal:
    breed: str
    name: str
    birth_date: datetime


@dataclass
class Person:
    name: str
    pet: Animal


p = Person(
    name='John',
    pet=Animal('Pig', 'Ham', datetime.now())
)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        elif isinstance(obj, datetime):
            return datetime.strftime(obj, '%Y-%m-%d')
        else:
            return obj

output = json.dumps([p], cls=CustomJSONEncoder)
print(output)
t = json.loads(output)
for i in t:
    print('KKK', i)
    p=Person(**i)
    print(p)
print(json.loads(output, object_hook=as_complex))

from pydantic import UrlStr
from pydantic.dataclasses import dataclass

@dataclass
class NavbarButton:
    href: UrlStr

@dataclass
class Navbar:
    button: NavbarButton

navbar = Navbar(button={'href':'https://example.com'})
print(navbar)
print(Person(name='test', pet={'breed': 'test', 'name': 'pig', 'birth_date': '2018-09-10'}))

exit(1)




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
    },
    marshallers={
        'application/json': DefaultJson
    }
)


if __name__ == '__main__':
    app.start()
