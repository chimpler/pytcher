import json
from abc import abstractmethod


class Unmarshaller(object):
    @abstractmethod
    def unmarshall(self, data: str, content_type='application/json', charset='utf-8'):
        pass


class DefaultJSONUnmarshaller(Unmarshaller):
    @abstractmethod
    def unmarshall(self, data: str):
        return json.loads(data)
