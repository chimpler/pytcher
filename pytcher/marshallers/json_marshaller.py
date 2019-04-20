import dataclasses
import json
from email import encoders
from json import JSONEncoder
from typing import Iterable

from pytcher.marshallers import encode, Marshaller


class EntityJSONEncoder(JSONEncoder):

    def __init__(self, *args, encoders=[], **kwargs):
        super(EntityJSONEncoder, self).__init__(*args, **kwargs)
        self._encoders = encoders

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
            try:
                return encode(obj, encoders)
            except StopIteration as e:
                return str(e)

    def encode_dict(self, dict_obj):
        return {
            key: self.default(value)
            for key, value in dict_obj.items()
        }


class EntityJSONEncoderBuilder(object):
    def __init__(self, **kwargs):
        super(EntityJSONEncoderBuilder, self).__init__()
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return EntityJSONEncoder(*args, **{**kwargs, **self._kwargs})


class JSONMarshaller(Marshaller):
    def marshall(self, obj):
        return json.dumps(
            obj,
            cls=EntityJSONEncoderBuilder(encoders=self._encoders, separators=(',', ':')),
        )
