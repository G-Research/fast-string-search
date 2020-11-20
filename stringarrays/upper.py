import time
import numpy as np
import pandas as pd

STRINGS = ["{} hello world how are you".format(i) for i in range(1_000_000)]


class ListStringArray:
    def __init__(self, values: list):
        self.array : list = values

    def __getitem__(self, i: int) -> str:
        return self.array[i]

    def upper(self) -> "ListStringArray":
        return ListStringArray([s.upper() for s in self.array])


class NumPyStringArray:
    def __init__(self, values):
        self.array = np.ndarray((len(values),), dtype=np.object)
        for i, v in enumerate(values):
            self.array[i] = v

    def __getitem__(self, i):
        return self.array[i]

    def upper(self):
        array = np.ndarray((len(self.array),), dtype=np.object)
        for i in range(len(array)):
            array[i] = self.array[i].upper()
        result = NumPyStringArray.__new__(NumPyStringArray)
        result.array = array
        return result


class ContiguousStringArray:
    def __init__(self, values):
        self.data = "".join(values)
        self.indexes = np.cumsum([0] + [len(v) for v in values], dtype=np.uint32)

    def __getitem__(self, i):
        start, end = self.indexes[i : i + 2]
        return self.data[start:end]

    def upper(self):
        data = self.data.upper()
        indexes = self.indexes[:]
        result = ContiguousStringArray.__new__(ContiguousStringArray)
        result.data = data
        result.indexes = indexes
        return result


def benchmark(what, f, *args, **kwargs):
    print(f"== Measuring {what} ==")
    start = time.time()
    f(*args, **kwargs)
    print(f"→ {what} took {time.time() - start}\n")


def run_with_class(klass):
    arr = klass(STRINGS)
    print("    ", arr[2], arr[356])
    start = time.time()
    arr = arr.upper()
    print(f"→ upper() took {time.time() - start}")
    print("    ", arr[2], arr[356])


def pandas():
    series = pd.Series(STRINGS)
    print("    ", series.iloc[2], series.iloc[356])
    start = time.time()
    #series2 = series.str.upper()
    series2 = pd.Series(s.upper() for s in series.tolist())
    print(f"→ upper() took {time.time() - start}")
    print("    ", series2.iloc[2], series2.iloc[356])

benchmark("Pandas", pandas)
benchmark("NumPy array of strings", run_with_class, NumPyStringArray)
benchmark("List of strings", run_with_class, ListStringArray)
benchmark("Contiguous string", run_with_class, ContiguousStringArray)
