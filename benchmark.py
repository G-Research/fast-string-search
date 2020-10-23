import timeit
import time

KEYS = ["abc", "hello", "world", "aardvark", "fish", "what", "arbitrarymonkey", "birds"]
KEYS += ["host%d" % i for i in range(500)]

LINE = "arbitrarymonkey says hello to fish host76, my friend, but why???"


def benchmark_regex(LINE):
    import re

    regex = re.compile("|".join(KEYS))
    LINE = LINE
    # Slight bug, finds host7 instead of host76... not critical for
    # benchmarking purposes though.
    print(regex.findall(LINE))
    start = time.time()
    timeit.timeit("regex.findall(LINE)", globals=locals())
    print(time.time() - start)


def benchmark_regex_trie(LINE):
    from trie import Trie
    import re

    trie = Trie()
    for key in KEYS:
        trie.add(key)
    regex = re.compile(trie.pattern())
    print(regex.findall(LINE))

    start = time.time()
    timeit.timeit("regex.findall(LINE)", globals=locals())
    print(time.time() - start)


if __name__ == "__main__":
    print("Naive regex")
    benchmark_regex(LINE)
    print()

    print("Regex trie")
    benchmark_regex_trie(LINE)
    print()
