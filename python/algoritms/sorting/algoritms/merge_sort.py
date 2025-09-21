from sorting.base import BaseSorting, SortAlgFactory


@SortAlgFactory.register('merge_base')
class MergeBaseSort(BaseSorting):
    """Merge Sort (base sort, for small data)"""
    def __init__(self, data:list):
        super().__init__(data)

    def result(self) -> list:
        return self._merge(self.data)

    def _merge(self, data:list) -> list:
        if len(data) > 1:
            mid = len(data)//2
            left = data[:mid]
            right = data[mid:]

            self._merge(left)
            self._merge(right)

            a = 0
            b = 0
            c = 0

            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    data[c] = left[a]
                    a += 1
                else:
                    data[c] = right[b]
                    b += 1
                c += 1
            while a < len(left):
                data[c] = left[a]
                a += 1
                c += 1

            while b < len(right):
                data[c] = right[b]
                b += 1
                c += 1

            return data


@SortAlgFactory.register('merge_fast')
class MergeFastSort(BaseSorting):
    """Merge Sort - Optimized (Working with indexes, not slices), for bigger data"""
    def __init__(self, data:list):
        super().__init__(data)

    def result(self) -> list:
        self._merge_in_place(self.data, 0, len(self.data))
        return self.data

    def _merge_in_place(self, data: list, start: int, end: int):
        if end - start > 1:
            mid = (start + end) // 2
            self._merge_in_place(data, start, mid)
            self._merge_in_place(data, mid, end)
            self._merge_sorted_parts(data, start, mid, end)

    @staticmethod
    def _merge_sorted_parts(data: list, start: int, mid: int, end: int):
        left = data[start:mid]
        right = data[mid:end]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            data[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            data[k] = right[j]
            j += 1
            k += 1