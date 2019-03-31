import dataclasses
from enum import Enum
from typing import Iterable

from pytcher.marshallers import Marshaller


class XMLMarshaller(Marshaller):

    # TODO add namespace XMLInstance for xsi:nil
    def marshall_obj(self, obj):
        if isinstance(obj, (bool, int, float, str)):
            return obj
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, tuple) and hasattr(obj, '_fields') and hasattr(obj, '_asdict'):
            return self.encode_dict(obj.__name__, obj._asdict())
        elif dataclasses.is_dataclass(obj):
            return self.encode_dict(obj.__class__.__name__, dataclasses.asdict(obj))
        elif isinstance(obj, Iterable):
            return ''.join([
                self.marshall(child)
                for child in obj
            ])
        else:
            for obj_type, function in self._encoders.items():
                if isinstance(obj, obj_type):
                    return function(obj)

    def encode_dict(self, name, dict_obj):
        return f'<{name}>' + ''.join([
            f'<{key}>{self.marshall(value)}</{key}>' if value is not None else f'<{key} xsi:nil="true"/>'
            for key, value in dict_obj.items()
        ]) + f'</{name}>'

    def marshall(self, obj):
        return self.marshall_obj(obj)
