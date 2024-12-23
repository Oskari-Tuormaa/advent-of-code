import numpy as np

from numpy.typing import NDArray
from numba import njit

PART1_SAMPLE_ANSWER = 37327623
PART2_SAMPLE_ANSWER = 23


def get_input(file: str):
    with open(file, "r") as fd:
        return list(map(int, fd.read().strip().splitlines()))


@njit
def mix_n_prune(v: int, secret: int) -> int:
    return (v ^ secret) % 16777216


@njit
def next_secret(v: int) -> int:
    v = mix_n_prune(v * 64, v)
    v = mix_n_prune(v // 32, v)
    v = mix_n_prune(v * 2048, v)
    return v


@njit
def calc_nth_secret(v: int, n: int) -> int:
    for _ in range(n):
        v = next_secret(v)
    return v


@njit
def calculate_secrets(seed: int, to: int) -> NDArray:
    res = []
    for i in range(to):
        res.append(calc_nth_secret(seed, i))
    return np.array(res)


def part1(input_file: str):
    seeds = get_input(input_file)
    return sum(calc_nth_secret(v, 2000) for v in seeds)


def part2(input_file: str):
    seeds = get_input(input_file)

    print(calculate_secrets(seeds[0], 2000))

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
