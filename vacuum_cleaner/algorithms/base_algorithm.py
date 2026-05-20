from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    @abstractmethod
    def search(self, environment, start):
        pass