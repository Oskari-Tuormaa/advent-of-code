import numpy as np

from itertools import product

PART1_SAMPLE_ANSWER = 3
PART2_SAMPLE_ANSWER = 0


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    locks = []
    keys = []
    for raw_lockey in data.split("\n\n"):
        lockey = np.array(list(list(line) for line in raw_lockey.splitlines()), dtype=str).T
        heights = (lockey == '#').sum(axis=1)
        if lockey[0,0] == '#':
            locks.append(heights)
        else:
            keys.append(heights)
    return np.array(locks), np.array(keys)

def part1(input_file: str):
    locks, keys = get_input(input_file)
    lock_spaces = 7 - locks
    return sum(1 for lock,key in product(lock_spaces, keys) if not ((lock-key)<0).any())


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
