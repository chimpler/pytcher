import json
from abc import abstractmethod


class Marshaller(object):

    @abstractmethod
    def marshall(self):
        pass


class DefaultJSONMarshaller(Marshaller):
    def marshall(self, obj):
        # TODO pass options for formatting
        return json.dumps(obj)
