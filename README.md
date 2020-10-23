# Fast substring search

## Problem statement

* We have 100M lines (strings).
* We have 5K keys (strings).
* For each line, we want to know which specific keys are in that line, if any, as quickly as possible.

The set of lines changes frequently.

## Approaches

### Regex

Search for "key1|key2|key3|etc.". This is slow.

### Regex constructed from trie

Create a trie, then a regex from that: https://stackoverflow.com/questions/42742810/speed-up-millions-of-regex-replacements-in-python-3/42789508#42789508

### Hash map/set (has additional restrictions)

Assumes lines can be split into words that can map to keys. You can then check each of those words against the hashed set of keys.

https://stackoverflow.com/a/42747503/6214034

### FlashText (has additional restrictions)

Assumes lines can be split into words that can map to keys.

Pure Python implementation: https://github.com/vi3k6i5/flashtext

### Aho-Corasick

Bit like FlashText, only doesn't have the boundary restriction, can do substrings too.

C + Python implementation: https://pypi.org/project/pyahocorasick/
Rust implementation (w/SIMD): https://github.com/BurntSushi/aho-corasick

## Second-pass optimizations, if necessary

Given this will be used with Pandas, bypassing Python functions altogether to iterate over the strings directly would speed things up.
Specifically, the code would iterate over NumPy object arrays; there are also Pandas StringArrays but apparently they're still experimental.
