import dataclasses
import itertools
from enum import Enum
from typing import Iterable

from pytcher.marshallers import Marshaller, MarshallerException


class CSVMarshaller(Marshaller):

    def encode_value(self, obj):
        if obj is None:
            return ''
        elif isinstance(obj, (bool, int, float, str)):
            return obj
        else:
            return next(
                (
                    encode(obj)
                    for condition, encode in self._encoders
                    if condition(obj)
                ),
                str(obj)
            )

    def encode_obj(self, obj_dict, columns):
        # TODO: create an iterator, escape chars and separator
        return ','.join(
            [
                str(obj_dict[col])
                for col in columns
            ]
        )

    def marshall(self, obj):
        it = iter(obj) if isinstance(obj, Iterable) else iter([obj])

        first_obj = next(it, None)
        if not first_obj:
            return ''

        if isinstance(first_obj, dict):
            extract_dict = lambda x: x  # noqa: E731
        elif isinstance(first_obj, tuple) and hasattr(first_obj, '_fields') and hasattr(first_obj, '_asdict'):
            extract_dict = lambda x: x._asdict()  # noqa: E731
        elif dataclasses.is_dataclass(first_obj):
            extract_dict = dataclasses.asdict
        else:
            raise MarshallerException(
                'Object type of {obj} must be of type dict (got {type}), namedtuple or dataclass'.format(
                    obj=first_obj,
                    type=type(first_obj)
                )
            )

        columns = extract_dict(first_obj).keys()

        # TODO: create an iterator, escape chars
        return '\n'.join(
            [','.join(columns)] + [
                self.encode_obj(extract_dict(obj), columns)
                for obj in itertools.chain([first_obj], it)
            ]
        )
