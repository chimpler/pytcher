import dataclasses


# TODO add custom decoder (datetime, ...)
class JSONDecoder(object):
    def decode(self, obj_type, obj):
        if obj is None:
            return None
        elif obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        elif obj_type.__module__ == 'typing':
            if obj_type.__origin__ is list:
                return [
                    self.decode(obj_type.__args__[0], e)
                    for e in obj
                ]
            elif obj_type.__origin__ is dict:
                return {
                    self.decode(obj_type.__args__[0], k): self.decode(obj_type.__args__[1], e)
                    for k, e in obj.items()
                }
        elif dataclasses.is_dataclass(obj_type):
            kwargs = {
                field.name: self.decode(field.type, obj[field.name])
                for field in dataclasses.fields(obj_type)
            }
            obj = obj_type(**kwargs)

            return obj
        else:
            return obj
