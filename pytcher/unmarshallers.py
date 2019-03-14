import json
from abc import abstractmethod


class Unmarshaller(object):
    @abstractmethod
    def unmarshall(self, data: str):
        pass


class DefaultJSONUnmarshaller(Unmarshaller):
    @abstractmethod
    def unmarshall(self, data: str):
        return json.loads(data)
