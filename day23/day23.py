import numpy as np

from numba import njit
from itertools import combinations
from numpy.typing import NDArray
from typing import Generator

PART1_SAMPLE_ANSWER = 7
PART2_SAMPLE_ANSWER = 0


def get_input(file: str):
    with open(file, "r") as fd:
        # return np.array(list(l.split('-') for l in fd.read().strip().splitlines()))
        data = list(l.split('-') for l in fd.read().strip().splitlines())

    computers = dict()
    for lhs, rhs in data:
        if lhs not in computers:
            computers[lhs] = set()
        if rhs not in computers:
            computers[rhs] = set()
        computers[lhs].add(rhs)
        computers[rhs].add(lhs)
    return computers



def yield_trios(connections: dict[str, set[str]]) -> Generator[set[str], None, None]:
    done = []
    for comp, conn in connections.items():
        for c1, c2 in combinations(conn, 2):
            if c1 in connections[c2] and {comp, c1, c2} not in done:
                done.append({comp, c1, c2})
                yield {comp, c1, c2}


def part1(input_file: str):
    connections = get_input(input_file)

    res = 0
    for trio in yield_trios(connections):
        if any(comp.startswith('t') for comp in trio):
            res += 1

    return res


def part2(input_file: str):
    inp = get_input(input_file)
    return 0


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
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, "input.txt")
    print(f"Part 2 --- Input [{dt:9.5f}s]: {sol}")
