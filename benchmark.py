import timeit
import time

KEYS = ["abc", "hello", "world", "aardvark", "fish", "what", "arbitrarymonkey", "birds"]
KEYS += ["host%d" % i for i in range(500)]

LINE = "arbitrarymonkey says hello to fish host76, my friend, but why???"


def benchmark(statement, variables):
    start = time.time()
    timeit.timeit(statement, globals=variables)
    print(time.time() - start)


def benchmark_regex(LINE):
    import re

    regex = re.compile("|".join(KEYS))
    LINE = LINE
    # Slight bug, finds host7 instead of host76... not critical for
    # benchmarking purposes though.
    print(regex.findall(LINE))

    benchmark("regex.findall(LINE)", locals())


def benchmark_regex_trie(LINE):
    from trie import Trie
    import re

    trie = Trie()
    for key in KEYS:
        trie.add(key)
    regex = re.compile(trie.pattern())
    print(regex.findall(LINE))

    benchmark("regex.findall(LINE)", locals())


def benchmark_pyahocorasick(LINE):
    from ahocorasick import Automaton, STORE_INTS

    automaton = Automaton()
    for i, key in enumerate(KEYS):
        automaton.add_word(key, key)
    automaton.make_automaton()

    print(list(automaton.iter(LINE)))

    benchmark("list(automaton.iter(LINE))", locals())


def benchmark_rustac(LINE):
    from pyrustac import ahocorasick

    # TODO This is ... inefficient, should be done better
    keys = "|".join(KEYS)
    print(ahocorasick(LINE, keys))

    benchmark("ahocorasick(LINE, keys)", locals())


if __name__ == "__main__":
    print("Regex trie")
    benchmark_regex_trie(LINE)
    print()

    print("pyahocorasick")
    benchmark_pyahocorasick(LINE)
    print()

    print("Rust aho-corasick")
    benchmark_rustac(LINE)
    print()

    print("Naive regex")
    benchmark_regex(LINE)
    print()
