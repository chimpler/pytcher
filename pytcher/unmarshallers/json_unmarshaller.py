import dataclasses
import json
from typing import TypeVar

from pytcher import UnmarshallException
from pytcher.unmarshallers import decode


class JSONUnmarshaller(object):
    def __init__(self, decoders=[]):
        self._decoders = decoders

    def make_obj(self, obj_type, obj):
        if obj_type is None:
            return obj
        elif obj is None:
            return None
        elif isinstance(obj, bool) and obj_type == bool:
            return obj
        elif isinstance(obj, int) and obj_type in (int, float):
            return obj
        elif isinstance(obj, float) and obj_type == float:
            return obj
        elif isinstance(obj, str) and obj_type == str:
            return obj
        elif obj_type.__module__ == 'typing':
            if isinstance(obj_type, TypeVar):
                return obj
            elif obj_type.__origin__ is list:
                return [
                    self.make_obj(obj_type.__args__[0], e)
                    for e in obj
                ]
            elif obj_type.__origin__ is dict:
                return {
                    self.make_obj(obj_type.__args__[0], k): self.make_obj(obj_type.__args__[1], e)
                    for k, e in obj.items()
                }
        elif dataclasses.is_dataclass(obj_type):
            kwargs = {
                field.name: self.make_obj(field.type, obj[field.name])
                for field in dataclasses.fields(obj_type)
            }
            obj = obj_type(**kwargs)
            return obj
        else:
            try:
                return decode(obj_type, obj, self._decoders)
            except StopIteration:
                raise UnmarshallException(
                    "Cannot decode '{obj}' with type '{type}'".format(obj=obj, type=obj_type.__name__))

    def unmarshall(self, obj_type, data):
        obj_dict = json.loads(data)
        return self.make_obj(obj_type, obj_dict)
