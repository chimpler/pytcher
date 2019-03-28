from abc import abstractmethod


class Unmarshaller(object):

    @abstractmethod
    def unmarshall(self, obj_type, obj):
        pass
