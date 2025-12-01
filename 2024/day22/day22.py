import numpy as np

from numpy.lib.stride_tricks import sliding_window_view
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
def calc_nth_secret(v: int, n: int):
    for _ in range(n):
        yield v
        v = next_secret(v)
    yield v


def part1(input_file: str):
    seeds = get_input(input_file)
    return sum(list(calc_nth_secret(v, 2000))[-1] for v in seeds)


def part2(input_file: str):
    seeds = get_input(input_file)

    price_history = []
    for seed in seeds:
        price_history.append(list(calc_nth_secret(seed, 2000)))
    price_history = np.array(price_history) % 10

    diff_total_yields = dict()
    for seller in price_history:

        diff_yields = {}
        diff = seller[1:] - seller[:-1]
        for v, d in zip(seller[4:], sliding_window_view(diff, 4)):
            d = tuple(int(x) for x in d)
            if d not in diff_yields:
                diff_yields[d] = int(v)

        for k, v in diff_yields.items():
            if k not in diff_total_yields:
                diff_total_yields[k] = 0
            diff_total_yields[k] += v

    d, v = max(diff_total_yields.items(), key=lambda x: x[1])
    return v


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
    sol, dt = run(part1, "sample1.txt")
    print(f"Part 1 -- Sample [{dt:9.5f}s]: {sol}")
    assert sol == PART1_SAMPLE_ANSWER, f"{sol} != {PART1_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part1, "input.txt")
    print(f"Part 1 --- Input [{dt:9.5f}s]: {sol}")

    print()
    sol, dt = run(part2, "sample2.txt")
    print(f"Part 2 -- Sample [{dt:9.5f}s]: {sol}")
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, "input.txt")
    print(f"Part 2 --- Input [{dt:9.5f}s]: {sol}")
