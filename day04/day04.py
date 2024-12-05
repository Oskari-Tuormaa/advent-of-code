import numpy as np
from numpy.typing import NDArray
import re

XMAS_SAMX_PATTERN = re.compile(r"(?=XMAS|SAMX)")
X_MAS_DIAGONAL_PATTERN = re.compile(r"M.M.A.S.S|S.M.A.S.M|M.S.A.M.S|S.S.A.M.M")

def get_input(file: str):
    with open(file, "r") as fd:
        return fd.readlines()


def traverse_all_angles(inp: NDArray, should_rotate: bool = True):
    # Horizontal
    for line in inp:
        yield ''.join(line)

    # Negative diagonal
    w, h = inp.shape
    for i in range(-h+1, w):
        yield ''.join(inp.diagonal(i))

    # Do the same on the rotated input array
    if should_rotate:
        yield from traverse_all_angles(np.rot90(inp), should_rotate=False)


def part1(input_file: str):
    inp = get_input(input_file)
    data = np.array([[y for y in x.strip()] for x in inp])

    res = 0
    for line in traverse_all_angles(data):
        res += len(XMAS_SAMX_PATTERN.findall(line))

    return res

def traverse_3x3(inp: NDArray):
    w, h = inp.shape
    for x in range(w-2):
        for y in range(h-2):
            yield inp[y:y+3,x:x+3]


def part2(input_file: str):
    inp = get_input(input_file)
    data = np.array([[y for y in x.strip()] for x in inp])

    count = 0
    for block in traverse_3x3(data):
        block_str = "".join(y for x in block for y in x)
        if X_MAS_DIAGONAL_PATTERN.match(block_str):
            count += 1

    return count


if __name__ == "__main__":
    print("Part 1 -- Sample:", part1("sample.txt"))
    print("Part 1 --- Input:", part1("input.txt"))

    print()
    print("Part 2 -- Sample:", part2("sample.txt"))
    print("Part 2 --- Input:", part2("input.txt"))
