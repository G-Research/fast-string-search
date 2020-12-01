import pandas as pd
import time

import pyximport
import numpy as np
import numba
from numba.typed import List as NumbaList

pyximport.install(language_level=3)

import cython_transform


STRINGS = ["{} hello world how are you".format(i) for i in range(1_000_000)]
SERIES = pd.Series(STRINGS)
unicode_array = SERIES.values.astype(np.unicode_)
bytes_array = np.array([s.encode("ascii") for s in SERIES.values], dtype=np.bytes_)


def measure(what, f):
    start = time.time()
    f()
    print(f"{what} elapsed: {time.time() - start}")


def replace_then_upper(s: str) -> str:
    return s.replace("l", "").upper()[1:-1]


@numba.njit
def _numba_replace_then_upper(in_arr):
    return [s.replace("l", "").upper()[1:-1] for s in in_arr]

def numba_apply(s: pd.Series, f) -> pd.Series:
    result = f(NumbaList(s.values))
    return pd.Series(result)


measure("Pandas apply()", lambda: SERIES.apply(replace_then_upper))
measure(
    "Pandas tolist()",
    lambda: pd.Series(replace_then_upper(s) for s in SERIES.tolist()),
)
measure(
    "Pandas .str",
    lambda: SERIES.str.replace("l", "").str.upper(),
)
measure(
    "Cython (naive)",
    lambda: pd.Series(cython_transform.transform_replace_then_upper(SERIES.values)),
)
measure(
    "Cython (memoryview)",
    lambda: pd.Series(
        cython_transform.transform_memoryview_replace_then_upper(SERIES.values)
    ),
)
# measure("Numba (first time)", lambda: numba_apply(SERIES, _numba_replace_then_upper))
# measure("Numba (second time)", lambda: numba_apply(SERIES, _numba_replace_then_upper))

# Technically cheating, but one could probably have extension array for Pandas
# with this kind of array.
measure(
    "NumPy np.char (unicode)",
    lambda: pd.Series(np.char.upper(np.char.replace(unicode_array, "l", ""))),
)
measure(
    "NumPy np.char (bytes)",
    lambda: pd.Series(np.char.upper(np.char.replace(bytes_array, b"l", b""))),
)
