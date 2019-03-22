import json
from abc import abstractmethod

from pytcher.encoders.json_encoder import JSONEncoder


class Marshaller(object):

    @abstractmethod
    def marshall(self):
        pass


class DefaultJSONMarshaller(Marshaller):
    def marshall(self, obj):
        return JSONEncoder().encode(obj)