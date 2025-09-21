from .base_sorting import BaseSorting


class SortAlgFactory:
    _reg = {}

    @classmethod
    def register(cls, name:str):
        def decorator(sort_class):
            if not issubclass(sort_class, BaseSorting):
                raise TypeError("Sort class must be a subclass of BaseSorting")
            if name in cls._reg:
                raise ValueError(f"Algorithm '{name}' already registered")
            cls._reg[name] = sort_class
            return sort_class
        return decorator

    def __init__(self, name:str):
        self.name = name

    def __call__(self, data):
        if not self.name in self._reg:
            raise ValueError("No module named " + self.name)
        return self._reg[self.name](data)

def return_algoritm(name:str, data:list):
    factory = SortAlgFactory(name)
    result = factory(data)
    return result()