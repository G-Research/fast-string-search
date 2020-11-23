import pandas as pd
import time

import pyximport

pyximport.install(language_level=3)

import numpy as np

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


measure("Pandas apply()", lambda: SERIES.apply(replace_then_upper))
measure(
    "Pandas tolist()",
    lambda: pd.Series(replace_then_upper(s) for s in SERIES.tolist()),
)
measure(
    "Pandas .str", lambda: SERIES.str.replace("l", "").str.upper(),
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
