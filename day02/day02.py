import numpy as np
from numpy.typing import NDArray

def get_input(file: str):
    with open(file, 'r') as fd:
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
        report_slice = np.concatenate((report[:i], report[i+1:]))
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


if __name__ == "__main__":
    print("Part 1 -- Sample:", part1("sample.txt"))
    print("Part 1 --- Input:", part1("input.txt"))

    print()
    print("Part 2 -- Sample:", part2("sample.txt"))
    print("Part 2 --- Input:", part2("input.txt"))
