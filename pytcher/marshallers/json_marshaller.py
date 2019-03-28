import dataclasses
import json
from enum import Enum
from json import JSONEncoder
from typing import Iterable, Tuple, Callable, List

from pytcher.marshallers import Marshaller, default_encoders


class EntityJSONEncoder(JSONEncoder):
    def __init__(self, *args, encoders=[], **kwargs):
        self._encoders = default_encoders + encoders
        super(EntityJSONEncoder, self).__init__(*args, **kwargs)

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
            return next(
                (
                    encode(obj)
                    for condition, encode in self._encoders
                    if condition(obj)
                ),
                obj
            )

    def encode_dict(self, dict_obj):
        return {
            key: self.default(value)
            for key, value in dict_obj.items()
        }

class EntityJSONEncoderBuilder(object):
    def __init__(self, encoders):
        self._encoders = encoders

    def __call__(self, *args, encoders={}, **kwargs):
        return EntityJSONEncoder(encoders=encoders)


class JSONMarshaller(Marshaller):
    def __init__(self, encoders: List[Tuple[Callable, Callable]] = []):
        self._encoders = encoders

    def marshall(self, obj):
        return json.dumps(obj, cls=EntityJSONEncoderBuilder(self._encoders))