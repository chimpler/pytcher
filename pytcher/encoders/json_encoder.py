import dataclasses
import json
import json as pyjson
from enum import Enum
from typing import Iterable


class CustomJSONEncoder(pyjson.JSONEncoder):

    def __init__(self, *args, **kwargs):
        if 'encoders' in kwargs:
            self._encoders = kwargs.get('encoders', {})
            del kwargs['encoders']
        else:
            self._encoders = {}

        super(CustomJSONEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, tuple) and hasattr(obj, '_fields') and hasattr(obj, '_asdict'):
            return self.encode_dict(obj._asdict())
        elif dataclasses.is_dataclass(obj):
            return self.encode_dict(dataclasses.asdict(obj))
        elif isinstance(obj, Iterable):
            return [
                self.default(child) for child in obj
            ]
        else:
            for obj_type, function in self._encoders.items():
                if isinstance(obj, obj_type):
                    return function(obj)

    def encode_dict(self, dict_obj):
        return {
            key: self.default(value)
            for key, value in dict_obj.items()
        }


class CustomJSONEncoderBuilder(object):
    def __init__(self, encoders=[]):
        self._encoders = encoders

    def __call__(self, *args, **kwargs):
        new_kwargs = {
            **kwargs,
            **{'encoders': self._encoders}
        }
        return CustomJSONEncoder(*args, **new_kwargs)


# TODO add custom decoder (datetime, ...)
class JSONEncoder(object):
    def encode(self, obj):
        return json.dumps(obj, cls=CustomJSONEncoderBuilder())
