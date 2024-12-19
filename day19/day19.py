import re

import numpy as np

from typing import Generator

PART1_SAMPLE_ANSWER = 6
PART2_SAMPLE_ANSWER = 16


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    towels, pattern = data.split("\n\n")

    return (
        re.findall(r'[^, ]+', towels),
        pattern.splitlines()
    )


class cache:
    def __init__(self, func):
        self.func = func
        self.cache = dict()
    def __call__(self, pattern: str, *args, **kwargs):
        if pattern not in self.cache:
            self.cache[pattern] = self.func(pattern, *args, **kwargs)
        return self.cache[pattern]
    def clear_cache(self):
        self.cache.clear()


@cache
def yield_arrangements(pattern: str, towels: list[str], yield_all: bool = False, depth: int = 0) -> int:
    res = 0
    if len(pattern) == 0:
        return 1
    for towel in towels:
        if pattern.startswith(towel):
            rest = pattern[len(towel):]
            viable_towels = [t for t in towels if t in rest]

            if yield_all:
                res += yield_arrangements(rest, viable_towels, yield_all=yield_all, depth=depth+1)
            else:
                return yield_arrangements(rest, viable_towels, yield_all=yield_all, depth=depth+1)
    return res


def part1(input_file: str):
    towels, patterns = get_input(input_file)
    towels = sorted(towels, key=lambda t: len(t), reverse=True)
    return sum(yield_arrangements(p, [t for t in towels if t in p]) for p in patterns)


def part2(input_file: str):
    towels, patterns = get_input(input_file)
    towels = sorted(towels, key=lambda t: len(t), reverse=True)
    yield_arrangements.clear_cache()
    return sum(yield_arrangements(p, [t for t in towels if t in p], yield_all=True) for p in patterns)


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
    print(f"Part 1 -- Sample [{dt:6.2f}s]: {sol}")
    assert sol == PART1_SAMPLE_ANSWER, f"{sol} != {PART1_SAMPLE_ANSWER}"

    # with nostdout():
    sol, dt = run(part1, "input.txt")
    print(f"Part 1 --- Input [{dt:6.2f}s]: {sol}")

    print()
    sol, dt = run(part2, "sample.txt")
    print(f"Part 2 -- Sample [{dt:6.2f}s]: {sol}")
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, "input.txt")
    print(f"Part 2 --- Input [{dt:6.2f}s]: {sol}")
