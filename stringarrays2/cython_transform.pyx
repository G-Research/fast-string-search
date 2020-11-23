cimport cython
cimport numpy as np
import numpy as np

ctypedef str (*string_transform)(str)


cdef np.ndarray transform(np.ndarray arr, string_transform f):
    cdef np.ndarray result
    cdef int i
    cdef str s
    result = np.ndarray((len(arr),), dtype=np.object)
    for i in range(len(arr)):
        s = arr[i]
        result[i] = f(s)
    return result


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef np.ndarray transform_memoryview(str[:] arr, string_transform f):
    cdef str[:] result_view
    cdef Py_ssize_t i
    cdef str s
    result = np.ndarray((len(arr),), dtype=object)
    result_view = result
    for i in range(len(arr)):
        s = arr[i]
        result_view[i] = f(s)
    return result


cdef str replace_then_upper(str s):
    return s.replace("l", "").upper()


def transform_replace_then_upper(arr: np.ndarray) -> np.ndarray:
    return transform(arr, replace_then_upper)

def transform_memoryview_replace_then_upper(str[:] arr) -> np.ndarray:
    return transform_memoryview(arr, replace_then_upper)
