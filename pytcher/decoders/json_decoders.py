import dataclasses
import json
from dataclasses import dataclass
from json.decoder import WHITESPACE


@dataclass
class Pet(object):
    breed: str

@dataclass
class Person(object):
    name: str
    age: int
    pet: Pet

for field in dataclasses.fields(Person):
    print(field)

def decode(obj_type, json_dict):
    if dataclasses.is_dataclass(obj_type):
        kwargs = {
            field.name: decode(field.type, json_dict[field.name])
            for field in dataclasses.fields(obj_type)
        }
        print(kwargs)
        obj = obj_type(**kwargs)

        return obj
    else:
        return json_dict

print(decode(Person, t))