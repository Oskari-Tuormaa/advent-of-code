import numpy as np

def get_input(file: str):
    with open(file, 'r') as fd:
        return fd.readlines()


def part1(input_file: str):
    inp = get_input(input_file)
    data = np.array([[int(y) for y in x.split()] for x in inp]).T
    data.sort()
    return abs(data[1] - data[0]).sum()


def part2(input_file: str):
    inp = get_input(input_file)
    data = np.array([[int(y) for y in x.split()] for x in inp]).T
    return np.array([x * (x == data[1]).sum() for x in data[0]]).sum()


if __name__ == "__main__":
    print("Part 1 -- Sample:", part1("sample.txt"))
    print("Part 1 --- Input:", part1("input.txt"))

    print()
    print("Part 2 -- Sample:", part2("sample.txt"))
    print("Part 2 --- Input:", part2("input.txt"))





