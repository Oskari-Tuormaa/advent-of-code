import re
from numba import njit
import numpy as np

FIND_EQUATIONS_PATTERN = re.compile(r"(\d+): ((?:\d+ ?)+)\n")


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read()

    equations = []
    for res, inp in FIND_EQUATIONS_PATTERN.findall(data):
        equations.append([int(res), list(map(int, inp.split(" ")))])
    return equations



@njit()
def can_be_true(
    test_value: int,
    remaining_numbers: list[int],
    current_sum: None | int = None,
    concat: bool = False,
) -> bool:
    if len(remaining_numbers) == 0:
        if test_value == current_sum:
            return True
        return False
    nxt = remaining_numbers[0]
    rest = remaining_numbers[1:]

    # Try +
    curr = current_sum if current_sum is not None else 0
    if can_be_true(test_value, rest, curr + nxt, concat=concat):
        return True

    # Try +
    curr = current_sum if current_sum is not None else 1
    if can_be_true(test_value, rest, curr * nxt, concat=concat):
        return True

    # Try ||
    curr = current_sum if current_sum is not None else 0
    if concat:
        nxt_n_digits = np.floor(np.log10(nxt)) + 1
        if can_be_true(
            test_value, rest, curr * 10**nxt_n_digits + nxt, concat=concat
        ):
            return True

    return False


def part1(input_file: str):
    inp = get_input(input_file)

    res = 0
    for test_value, number in inp:
        if can_be_true(test_value, number):
            res += test_value

    return res


def part2(input_file: str):
    inp = get_input(input_file)

    res = 0
    for test_value, number in inp:
        if can_be_true(test_value, number, concat=True):
            res += test_value

    return res


if __name__ == "__main__":
    print("Part 1 -- Sample:", part1("sample.txt"))
    print("Part 1 --- Input:", part1("input.txt"))

    print()
    print("Part 2 -- Sample:", part2("sample.txt"))
    print("Part 2 --- Input:", part2("input.txt"))
