from sorting.base import BaseSorting, SortAlgFactory


@SortAlgFactory.register('bubble')
class BubbleSort(BaseSorting):
    """Bubble Sort"""
    def __init__(self, data:list):
        super().__init__(data)

    def result(self) -> list:
        last_el_index = len(self.data)-1
        for pass_no in range(last_el_index, 0, -1):
            for id in range(pass_no):
                print(f"Current element: {self.data[id]}, current list: {self.data}")
                if self.data[id] > self.data[id+1]:
                    self.data[id], self.data[id+1] = self.data[id+1], self.data[id]
                    print(f"Current moved element: {self.data[id]}, current moved list: {self.data}")

        return self.data