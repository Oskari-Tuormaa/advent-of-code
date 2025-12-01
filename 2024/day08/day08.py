from itertools import combinations
from typing import Generator

PART1_SAMPLE_ANSWER = 14
PART2_SAMPLE_ANSWER = 34


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read()

    nodes = dict()
    lines = data.splitlines()
    bounds = (len(lines[0]), len(lines))
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell != ".":
                if cell not in nodes:
                    nodes[cell] = set()
                nodes[cell].add((x, y))
    return nodes, bounds


def pos_within_bounds(pos: tuple[int, int], bounds: tuple[int, int]) -> bool:
    x, y = pos
    w, h = bounds
    return x >= 0 and y >= 0 and x < w and y < h


def yield_first_reflections(
    positions: list[tuple[int, int]]
) -> Generator[tuple[int, int], None, None]:
    for n1, n2 in combinations(positions, 2):
        x1, y1 = n1
        x2, y2 = n2
        dx = x2 - x1
        dy = y2 - y1

        yield x1 - dx, y1 - dy
        yield x2 + dx, y2 + dy


def yield_all_reflections_in_bounds(
    positions: list[tuple[int, int]], bounds: tuple[int, int]
) -> Generator[tuple[int, int], None, None]:
    for n1, n2 in combinations(positions, 2):
        x1, y1 = n1
        x2, y2 = n2
        dx = x2 - x1
        dy = y2 - y1

        p = (x1 - dx, y1 - dy)
        while pos_within_bounds(p, bounds):
            yield p
            p = (p[0] - dx, p[1] - dy)
        p = (x2 + dx, y2 + dy)
        while pos_within_bounds(p, bounds):
            yield p
            p = (p[0] + dx, p[1] + dy)


def part1(input_file: str):
    antennas, bounds = get_input(input_file)

    res = set()
    for nodes in antennas.values():
        for reflection in yield_first_reflections(nodes):
            if pos_within_bounds(reflection, bounds):
                res.add(reflection)

    return len(res)


def part2(input_file: str):
    antennas, bounds = get_input(input_file)

    res = set()
    for nodes in antennas.values():
        for reflection in yield_all_reflections_in_bounds(nodes, bounds):
            res.add(reflection)

    all_antennas = {x for ant in antennas.values() for x in ant}
    res = res.union(all_antennas)

    return len(res)


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
