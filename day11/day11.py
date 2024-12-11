import numba

import numpy as np

from functools import cache
from numpy.typing import NDArray

PART1_SAMPLE_ANSWER = 55312
PART2_SAMPLE_ANSWER = 65601038650482

SAMPLE_INPUT = np.array([125, 17])
PUZZLE_INPUT = np.array([2, 77706, 5847, 9258441, 0, 741, 883933, 12])


@numba.njit()
def n_digits(num: int) -> int:
    return np.floor(np.log10(num)) + 1


@numba.njit()
def try_split_num(num: int) -> tuple[int, int] | None:
    n_dig = n_digits(num)
    if n_dig % 2 == 1:
        return
    factor = int(10 ** (n_dig / 2))
    return (
        num // factor,
        num % factor,
    )


@cache
def count_resulting_stones(stone: int, depth: int) -> int:
    if depth == 0:
        return 1
    if stone == 0:
        return count_resulting_stones(1, depth - 1)
    if (s := try_split_num(stone)) is not None:
        return (count_resulting_stones(s[0], depth - 1) +
                count_resulting_stones(s[1], depth - 1))
    return count_resulting_stones(stone * 2024, depth - 1)


def part1(input: NDArray):
    return sum(map(lambda x: count_resulting_stones(x, 25), input))


def part2(input: NDArray):
    return sum(map(lambda x: count_resulting_stones(x, 75), input))


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

    sol, dt = run(part1, SAMPLE_INPUT)
    print(f"Part 1 -- Sample [{dt:6.2f}s]: {sol}")
    assert sol == PART1_SAMPLE_ANSWER, f"{sol} != {PART1_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part1, PUZZLE_INPUT)
    print(f"Part 1 --- Input [{dt:6.2f}s]: {sol}")

    print()
    sol, dt = run(part2, SAMPLE_INPUT)
    print(f"Part 2 -- Sample [{dt:6.2f}s]: {sol}")
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, PUZZLE_INPUT)
    print(f"Part 2 --- Input [{dt:6.2f}s]: {sol}")
