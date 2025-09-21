from abc import ABC, abstractmethod


class BaseSorting(ABC):
    def __init__(self, data):
        self.data = [int(x.strip()) for x in data]

    def __call__(self):
        return self.result()

    @abstractmethod
    def result(self) -> list:
        pass
