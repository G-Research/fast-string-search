cimport numpy as np

import time
import numpy as np
import pandas as pd

STRINGS = ["{} hello world how are you".format(i) for i in range(1_000_000)]


cdef class ListStringArray:
    cdef list array
    def __init__(self, list values):
        self.array = values

    def __getitem__(self, i: int) -> str:
        return self.array[i]

    def upper(self) -> "ListStringArray":
        cdef list l
        l = []
        cdef str s
        for s in self.array:
            l.append(s.upper())
        return ListStringArray(l)

ctypedef str (*string_transform)(str)

cdef class NumPyStringArray:

    cdef np.ndarray array

    def __init__(self, values):
        if isinstance(values, np.ndarray):
            self.array = values
        else:
            self.array = np.ndarray((len(values),), dtype=np.object)
            for i, v in enumerate(values):
                self.array[i] = v

    def __getitem__(self, i):
        return self.array[i]

    def upper(self):
        cdef np.ndarray array
        array = np.ndarray((len(self.array),), dtype=np.object)
        cdef int i
        cdef str s
        for i in range(len(array)):
            s = self.array[i]
            array[i] = s.upper()
        return NumPyStringArray(array)

    cdef apply(self, string_transform f):
        cdef np.ndarray array
        array = np.ndarray((len(self.array),), dtype=np.object)
        cdef int i
        cdef str s
        for i in range(len(array)):
            s = self.array[i]
            array[i] = f(s)
        return NumPyStringArray(array)


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


cdef str to_upper(str s):
    return s.upper()

def apply_numpy():
    print("== Measuring NumPy with apply() ==")
    cdef NumPyStringArray arr
    arr = NumPyStringArray(STRINGS)
    print("    ", arr[2], arr[356])
    start = time.time()
    arr = arr.apply(to_upper)
    print(f"→ upper() took {time.time() - start}")
    print("    ", arr[2], arr[356])
    print(f"→ took {time.time() - start}\n")

def run_with_numpy():
    cdef NumPyStringArray arr
    arr = NumPyStringArray(STRINGS)
    print("    ", arr[2], arr[356])
    start = time.time()
    arr = arr.upper()
    print(f"→ upper() took {time.time() - start}")
    print("    ", arr[2], arr[356])


def run_with_list():
    cdef ListStringArray arr
    arr = ListStringArray(STRINGS)
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
benchmark("NumPy array of strings", run_with_numpy)
benchmark("List of strings", run_with_list)
#benchmark("Contiguous string", run_with_class, ContiguousStringArray)
benchmark("NumPy array of strings, apply()", apply_numpy)
