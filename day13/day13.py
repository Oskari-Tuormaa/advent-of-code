import re

from itertools import starmap

import sympy as sp

PART1_SAMPLE_ANSWER = 480
PART2_SAMPLE_ANSWER = 875318608908

BTN_VALUES = sp.Matrix.diag([3, 1])


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    machines = []
    for machine in data.split("\n\n"):
        ax, ay, bx, by, x, y = map(int, re.findall(r"\d+", machine))
        machines.append([sp.Matrix([ax, ay]), sp.Matrix([bx, by]), sp.Matrix([x, y])])
    return machines


def change_of_basis(v1: sp.Matrix, v2: sp.Matrix, point: sp.Matrix):
    change_matrix = sp.Matrix([[*v1], [*v2]]).T.inv()
    return change_matrix * point


def part1(input_file: str):
    machines = get_input(input_file)

    return sum(
        sum(BTN_VALUES * bp)
        for bp in starmap(lambda a,b,p: change_of_basis(a,b,p), machines)
        if all(i.is_Integer for i in bp)
    )


def part2(input_file: str):
    machines = get_input(input_file)

    add = sp.Matrix([10000000000000] * 2)
    return sum(
        sum(BTN_VALUES * bp)
        for bp in starmap(lambda a,b,p: change_of_basis(a,b,p+add), machines)
        if all(i.is_Integer for i in bp)
    )


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
    print(f"Part 1 -- Sample [{dt:6.2f}s]: {sol}")
    assert sol == PART1_SAMPLE_ANSWER, f"{sol} != {PART1_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part1, "input.txt")
    print(f"Part 1 --- Input [{dt:6.2f}s]: {sol}")

    print()
    sol, dt = run(part2, "sample.txt")
    print(f"Part 2 -- Sample [{dt:6.2f}s]: {sol}")
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, "input.txt")
    print(f"Part 2 --- Input [{dt:6.2f}s]: {sol}")
