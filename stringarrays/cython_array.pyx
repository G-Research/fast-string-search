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


cdef str upper(str s):
    return s.upper()


def transform_upper(arr: np.ndarray) -> np.ndarray:
    return transform(arr, upper)
