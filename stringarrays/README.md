# String array experiment

## Problem statement

Pandas stores strings as a NumPy array of Python objects.

This means string operations involve iterating over an array, finding the Python object, calling the Python method on it.
Doing this iteration in Python is slow.
Doing a Python function call is also slow.
Following the pointer isn't as slow as the above, but even solving the above two you'd still have this as a performance hit.

The goal is a Pandas string array that is significantly faster.

## Discussion

Imagine if all the strings were in a contiguous chunk of memory, with a separate array tracking boundaries.

Some operations would be difficult to do efficiently... but most operations you are likely to do in Pandas would involve just creating a new contiguous chunk of memory with different results.

Other alternatives include ropes, and likely other data structures.

## Things to investigate

How slow is e.g. Python upper()? It's not slow at all, seemingly.

Is list-of-strings extension type really much faster than numpy aray/pandas? Why?

Try mypyc

Tradeoff between memory vs. CPU (operating on contiguous chunk when you have e.g. `lambda s: s.upper().strip()` will use more memory than operating on small strings).

Can cython go faster?

parallelism

numexpr!
