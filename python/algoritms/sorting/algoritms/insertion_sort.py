from sorting.base import BaseSorting, SortAlgFactory


@SortAlgFactory.register('insertion')
class InsertionSort(BaseSorting):
    """Insert Sort"""
    def __init__(self, data:list):
        super().__init__(data)

    def result(self) -> list:
        for i in range(1, len(self.data)):
            j = i-1
            element_next = self.data[i]
            while (self.data[j] > element_next) and (j >= 0):
                self.data[j+1] = self.data[j]
                j = j-1
            self.data[j+1] = element_next
        return self.data