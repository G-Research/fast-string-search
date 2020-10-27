from typing import Optional, Any
import timeit
import time
import random

KEYS = ["abc", "hello", "world", "aardvark", "fish", "what", "arbitrarymonkey", "birds"]
KEYS += ["host%d" % i for i in range(500)]
KEYS += [str(random.random()) for i in range(500)]

LINE = "arbitrarymonkey says hello to fish host76, 0.123 my friend, but why???"


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
    from pyrustac import AC

    # TODO This is ... inefficient, should be done better
    keys = "|".join(KEYS)
    ac = AC(keys)
    print(ac.findall(LINE))

    benchmark("ac.findall(LINE)", locals())


def benchmark_hyperscan(LINE):
    import hyperscan

    db = hyperscan.Database()
    db.compile(
        expressions=[k.encode("utf-8") for k in KEYS],
        ids=list(range(len(KEYS))),
        elements=len(KEYS),
        flags=0,
    )

    l = []

    def on_match(
        id: int, from_: int, to: int, flags: int, context: Optional[Any] = None
    ) -> Optional[bool]:
        l.append(id)

    LINE = LINE.encode("utf-8")
    db.scan(LINE, match_event_handler=on_match)
    print(l)

    # TODO the Python hyperscan API I found initially is extremely inefficient,
    # doing a Python callback on every match. So not doing any match handling
    # here, just to get a sense of raw performance.
    benchmark("db.scan(LINE)", locals())


def benchmark_flashtext(LINE):
    from flashtext import KeywordProcessor

    keyword_processor = KeywordProcessor()
    for key in KEYS:
        keyword_processor.add_keyword(key)

    print(keyword_processor.extract_keywords(LINE))

    benchmark("keyword_processor.extract_keywords(LINE)", locals())


def benchmark_flashtext_rust(LINE):
    from pyrustac import FT

    ft = FT()
    for key in KEYS:
        ft.add(key)

    print(ft.find_keywords(LINE))

    benchmark("ft.find_keywords(LINE)", locals())


def run(title, function):
    print(f"== {title} ==")
    function(LINE)
    print()


if __name__ == "__main__":
    run("Regex trie", benchmark_regex_trie)

    run("pyahocorasick", benchmark_pyahocorasick)

    run("Rust aho-corasick", benchmark_rustac)

    run("Hyperscan (see code for caveats)", benchmark_hyperscan)

    print("=== SKIPPING DUE TO SLOWNESS ===")
    print("FlashText (Rust)")
    # benchmark_flashtext_rust(LINE)

    print("Naive regex")
    # benchmark_regex(LINE)

    print("FlashText (in Python)")
    # benchmark_flashtext(LINE)
