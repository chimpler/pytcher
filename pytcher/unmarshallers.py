import json
from abc import abstractmethod

from pytcher.decoders.json_decoder import JSONDecoder


class Unmarshaller(object):
    @abstractmethod
    def unmarshall(self, obj_type, data: str, path=None):
        pass


class DefaultJSONUnmarshaller(Unmarshaller):
    @abstractmethod
    def unmarshall(self, obj_type, data: str, path=None):
        root = json.loads(data)
        # TODO filter on path
        return JSONDecoder().decode(obj_type, root)
