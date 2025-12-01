import re

from functools import cache
from itertools import zip_longest
from numba import njit

PART1_SAMPLE_ANSWER = "4,6,3,5,6,3,5,2,1,0"
PART2_SAMPLE_ANSWER = 117440


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    a, b, c, *opcodes = map(int, re.findall(r"\d+", data))
    opcodes = [(opc, ope) for opc,ope in zip(opcodes[::2], opcodes[1::2])]
    return a, b, c, opcodes


ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7


def run_program(a: int, b: int, c: int, opcodes: list[tuple[int, int]]):
    pc = 0

    def combo(n: int) -> int:
        if 0 <= n <= 3:
            return n
        if n == 4:
            return a
        if n == 5:
            return b
        if n == 6:
            return c
        raise ValueError

    while 0 <= pc < len(opcodes):
        opc, ope = opcodes[pc]

        if opc == ADV:
            a = a // 2**combo(ope)
        elif opc == BXL:
            b ^= ope
        elif opc == BST:
            b = combo(ope) % 8
        elif opc == JNZ:
            if a != 0:
                pc = ope//2
                continue
        elif opc == BXC:
            b = b^c
        elif opc == OUT:
            yield combo(ope) % 8
        elif opc == BDV:
            b = a // 2**combo(ope)
        elif opc == CDV:
            c = a // 2**combo(ope)

        pc += 1


def part1(input_file: str):
    prog = get_input(input_file)
    return ",".join(map(str, run_program(*prog)))


def find_solutions(prog: list[tuple[int, int]], opcodes: list[int], _from: int = 0, to: int = 8):
    code = opcodes[-1]
    for a in range(_from, to):
        n = next(run_program(a, 0, 0, prog))
        if n == code:
            if len(opcodes) == 1:
                return a
            if (res := find_solutions(prog, opcodes[:-1], a<<3, (a+1)<<3)) is not None:
                return res


def part2(input_file: str):
    _, _, _, opcodes = get_input(input_file)
    return find_solutions(opcodes, list(x for y in opcodes for x in y))


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
