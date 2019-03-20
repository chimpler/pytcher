import json
from abc import abstractmethod


class Marshaller(object):

    @abstractmethod
    def marshall(self):
        pass


class DefaultJSONMarshaller(Marshaller):
    def marshall(self, obj, charset='utf-8'):
        return json.dumps(obj)
