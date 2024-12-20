import numpy as np
from numpy.typing import NDArray

PART1_SAMPLE_ANSWER = 36
PART2_SAMPLE_ANSWER = 81


def get_input(file: str):
    with open(file, "r") as fd:
        return np.array(
            [
                list(-1 if x == "." else int(x) for x in line)
                for line in fd.read().strip().splitlines()
            ]
        )


def count_trails(map: NDArray, start_pos: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = start_pos

    if map[y, x] == 9:
        return [(x, y)]

    w, h = map.shape
    reachable_peaks = []

    for xx in range(max(0, x - 1), min(w - 1, x + 1) + 1):
        if map[y, xx] == map[y, x] + 1:
            reachable_peaks += count_trails(map, (xx, y))

    for yy in range(max(0, y - 1), min(h - 1, y + 1) + 1):
        if map[yy, x] == map[y, x] + 1:
            reachable_peaks += count_trails(map, (x, yy))

    return reachable_peaks


def part1(input_file: str):
    map = get_input(input_file)

    res = 0
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == 0:
                res += len(set(count_trails(map, (x, y))))
    return res


def part2(input_file: str):
    map = get_input(input_file)

    res = 0
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == 0:
                res += len(count_trails(map, (x, y)))

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
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, "input.txt")
    print(f"Part 2 --- Input [{dt:9.5f}s]: {sol}")
