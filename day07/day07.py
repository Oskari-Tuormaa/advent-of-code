import re

FIND_EQUATIONS_PATTERN = re.compile(r'(\d+): ((?:\d+ ?)+)\n')

def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read()

    equations = []
    for res, inp in FIND_EQUATIONS_PATTERN.findall(data):
        equations.append([int(res), list(map(int, inp.split(" ")))])
    return equations


def can_be_true(test_value: int, remaining_numbers: list[int], current_sum: int = 0, concat: bool = False) -> bool:
    if len(remaining_numbers) == 0:
        if test_value == current_sum:
            return True
        return False

    if current_sum == 0:
        a, b, *rest = remaining_numbers
        if can_be_true(test_value, rest, a + b, concat=concat):
            return True
        elif can_be_true(test_value, rest, a * b, concat=concat):
            return True
        elif concat and can_be_true(test_value, rest, int(str(a) + str(b)), concat=concat):
            return True
        return False

    nxt, *rest = remaining_numbers
    if can_be_true(test_value, rest, current_sum + nxt, concat=concat):
        return True
    elif can_be_true(test_value, rest, current_sum * nxt, concat=concat):
        return True
    elif concat and can_be_true(test_value, rest, int(str(current_sum) + str(nxt)), concat=concat):
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
