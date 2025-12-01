import numpy as np
from numpy.typing import NDArray

PART1_SAMPLE_ANSWER = 2
PART2_SAMPLE_ANSWER = 4


def get_input(file: str):
    with open(file, "r") as fd:
        return fd.readlines()


def is_safe(report: NDArray[np.int32]) -> bool | np.bool:
    diffs = report[1:] - report[:-1]

    all_inc_dec = (diffs > 0).all() | (diffs < 0).all()
    within_limits = ((1 <= abs(diffs)) & (abs(diffs) <= 3)).all()

    return all_inc_dec & within_limits


def part1(input_file: str):
    inp = get_input(input_file)

    sum = 0
    for line in inp:
        data = np.array([int(x) for x in line.split()])
        sum += is_safe(data)

    return sum


def try_dampener(report: NDArray[np.int32]) -> bool | np.bool:
    for i in range(len(report)):
        report_slice = np.concatenate((report[:i], report[i + 1 :]))
        if is_safe(report_slice):
            return True
    return False


def part2(input_file: str):
    inp = get_input(input_file)

    sum = 0
    for line in inp:
        data = np.array([int(x) for x in line.split()])
        if is_safe(data):
            sum += 1
        else:
            sum += try_dampener(data)

    return sum


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
