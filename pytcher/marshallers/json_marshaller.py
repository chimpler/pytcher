import dataclasses
import json
from email import encoders
from json import JSONEncoder
from typing import Iterable

from pytcher.marshallers import Marshaller, encode


class EntityJSONEncoder(JSONEncoder):

    def __init__(self, *args, encoders=[], **kwargs):
        self._encoders = encoders
        super(EntityJSONEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        elif isinstance(obj, tuple) and hasattr(obj, '_fields') and hasattr(obj, '_asdict'):
            return self.encode_dict(obj._asdict())
        elif dataclasses.is_dataclass(obj):
            return self.encode_dict(dataclasses.asdict(obj))
        elif isinstance(obj, Iterable):
            return [
                self.default(child) for child in obj
            ]
        else:
            return encode(obj, encoders)

    def encode_dict(self, dict_obj):
        return {
            key: self.default(value)
            for key, value in dict_obj.items()
        }


class EntityJSONEncoderBuilder(object):
    def __init__(self, encoders, **kwargs):
        self._encoders = encoders
        self._extra_args = kwargs

    def __call__(self, *args, encoders=[], **kwargs):
        return EntityJSONEncoder(*args, encoders=encoders, **{**kwargs, **self._extra_args})


class JSONMarshaller(Marshaller):

    def marshall(self, obj):
        return json.dumps(
            obj,
            cls=EntityJSONEncoderBuilder(encoders=self._encoders, separators=(',', ':')),
        )
