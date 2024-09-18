from itertools import chain

# Created by implementing the operations of Bjorklund's algorithm as described in:
# "Structural properties of Euclidean rhythms", 2009
# DOI: https://doi.org/10.1080/17459730902819566


def euc(onsets, subdivisions, rotation) -> list[int]:
    s = [[1] if i < onsets else [0] for i in range(subdivisions)]
    a = min(onsets, subdivisions - onsets)
    b = max(onsets, subdivisions - onsets)
    if a < 1:
        return list(chain.from_iterable(s))

    for i in range(b // a):
        for j in range(a):
            s[j].extend(s.pop())

    b = b % a

    while b > 1:
        for i in range(a // b):
            for j in range(b):
                s[j].extend(s.pop())
        temp = b
        b = a % b
        a = temp

    s = list(chain.from_iterable(s))
    return s[-rotation:] + s[:-rotation]
