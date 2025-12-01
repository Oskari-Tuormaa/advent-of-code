import re

from itertools import pairwise
from functools import cache

PART1_SAMPLE_ANSWER = 126384

coord = tuple[int, int]

KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", 'A']
]


DPAD = [
    [None, '^', 'A'],
    ['<', 'v', '>'],
]


def get_input(file: str):
    with open(file, "r") as fd:
        return fd.read().strip().splitlines()


def get_pos(arr: list[list[str|None]], code: str) -> coord:
    for y, row in enumerate(arr):
        if code in row:
            return (row.index(code), y)
    raise ValueError(f"{code} not found in {arr}")


@cache
def shortest_path_between(start: str | coord, end: str | coord, depth: int, first: bool = True) -> int:
    if depth == 0:
        return 1
    
    if isinstance(start, str):
        start = get_pos(KEYPAD if first else DPAD, start)
    if isinstance(end, str):
        end = get_pos(KEYPAD if first else DPAD, end)

    sx, sy = start
    ex, ey = end
    dx = abs(ex - sx) - 1
    dy = abs(ey - sy) - 1
    vert = None
    hori = None
    if ex > sx:
        hori = '>'
    elif ex < sx:
        hori = '<'
    if ey > sy:
        vert = 'v'
    elif ey < sy:
        vert = '^'

    nxt = lambda frm,to: shortest_path_between(frm,to,depth=depth-1,first=False)

    if hori is None and vert is None:
        return 1
    if hori is None and vert is not None:
        return sum([
            nxt('A', vert),
            dy,
            nxt(vert, 'A')
        ])
    if hori is not None and vert is None:
        return sum([
            nxt('A', hori),
            dx,
            nxt(hori, 'A')
        ])

    assert hori is not None and vert is not None

    if (first and sy == 3 and ex == 0) or (not first and ex == 0):
        return sum([
            nxt('A', vert),
            dy,
            nxt(vert, hori),
            dx,
            nxt(hori, 'A')
        ])
    if (first and ey == 3 and sx == 0) or (not first and sx == 0):
        return sum([
            nxt('A', hori),
            dx,
            nxt(hori, vert),
            dy,
            nxt(vert, 'A')
        ])
    return min([
        sum([
            nxt('A', vert),
            dy,
            nxt(vert, hori),
            dx,
            nxt(hori, 'A')
        ]),
        sum([
            nxt('A', hori),
            dx,
            nxt(hori, vert),
            dy,
            nxt(vert, 'A')
        ])
    ])


def extract_number(v: str) -> int:
    return int("".join(re.findall(r"\d+", v)))


def part1(input_file: str):
    codes = get_input(input_file)

    res = 0
    for code in codes:
        smallest_path = sum(
            shortest_path_between(frm, to, 3)
            for frm,to in pairwise('A'+code)
        )
        res += extract_number(code) * smallest_path

    return res


def part2(input_file: str):
    codes = get_input(input_file)

    res = 0
    for code in codes:
        smallest_path = sum(
            shortest_path_between(frm, to, 26)
            for frm,to in pairwise('A'+code)
        )
        res += extract_number(code) * smallest_path

    return res


#################################################
##                                             ##
##      Runner stuff beyond this point         ##
##                                             ##
#################################################
import sys, os, time, contextlib


def run(func, *args, **kwargs):
    t0 = time.time()
    return func(*args, **kwargs), time.time() - t0


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    yield
    sys.stdout = save_stdout


if __name__ == "__main__":
    sol, dt = run(part1, "sample.txt")
    print(f"Part 1 -- Sample [{dt:9.5f}s]: {sol}")
    assert sol == PART1_SAMPLE_ANSWER, f"{sol} != {PART1_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part1, "input.txt")
    print(f"Part 1 --- Input [{dt:9.5f}s]: {sol}")

    print()
    sol, dt = run(part2, "sample.txt")
    print(f"Part 2 -- Sample [{dt:9.5f}s]: {sol}")

    with nostdout():
        sol, dt = run(part2, "input.txt")
    print(f"Part 2 --- Input [{dt:9.5f}s]: {sol}")
