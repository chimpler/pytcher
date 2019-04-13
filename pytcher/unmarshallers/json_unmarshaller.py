import dataclasses
import json

from pytcher.unmarshallers import decode


class JSONUnmarshaller(object):
    def __init__(self, decoders=[]):
        self._decoders = decoders

    def make_obj(self, obj_type, obj):
        if obj is None:
            return None
        elif obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        elif obj_type.__module__ == 'typing':
            if obj_type.__origin__ is list:
                return [
                    self.make_obj(obj_type.__args__[0], e)
                    for e in obj
                ]
            elif obj_type.__origin__ is dict:
                return {
                    self.make_obj(obj_type.__args__[0], k): self.unmarshall(obj_type.__args__[1], e)
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
            return decode(obj_type, obj, self._decoders)

    def unmarshall(self, obj_type, data):
        obj_dict = json.loads(data)
        return self.make_obj(obj_type, obj_dict)
