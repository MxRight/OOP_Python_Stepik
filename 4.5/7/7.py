from abc import ABC, abstractmethod

class StackInterface(ABC):
    @abstractmethod
    def push_back(self, obj):
        """ """

    @abstractmethod
    def pop_back(self):
        """ """


class Stack(StackInterface):
    def __init__(self):
        self._top = None
        self.lst = []

    def push_back(self, obj):
        if self._top is None:
            self._top = obj
        else:
            self.lst[-1]._next = obj
        self.lst.append(obj)

    def pop_back(self):
        if len(self.lst)==1:
            self._top = None
        if len(self.lst)>1:
            self.lst[-2]._next = None
        if len(self.lst)>0:
            a = self.lst[-1]
            del self.lst[-1]
            
            return a
        else:
            return None


class StackObj:
    def __init__(self, data):
        self._data = data
        self._next = None
