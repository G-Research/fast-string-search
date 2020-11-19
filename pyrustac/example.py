import random

KEYS = ["abc", "hello", "world", "aardvark", "fish", "what", "arbitrarymonkey", "birds"]
KEYS += ["host%d" % i for i in range(500)]
KEYS += [str(random.random()) for i in range(500)]

LINE = "arbitrarymonkey says hello to fish host76, 0.123 my friend, but why???"


from pyrustac import AC

# TODO This is not the final API, just threw it together for testing purposes.
keys = "|".join(KEYS)
# Create Aho-Corasick datastructure with given keys:
ac = AC(keys)
# Find matching keys; return list of indexes. Notice it finds host7 but not
# host76. I think there's a flag to fix that (overlapping support, and there's
# also longest-matching support).
matches = ac.findall(LINE)
print(matches)

# For performance reasons I suggest sticking to the above in Pandas, or at
# least only doing this below for those lines that match. It can be done inside
# the library for higher performance, too.
print([KEYS[i] for i in matches])
