import re

import numpy as np

from numpy.typing import NDArray
from itertools import combinations

PART1_SAMPLE_ANSWER = 2024
PART2_SAMPLE_ANSWER = 0


GATE_TYPE = 0
GATE_LHS = 1
GATE_RHS = 2
GATE_OUT = 3


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    raw_initial_values, raw_gates = data.split("\n\n")

    initial_values = dict()
    for v in raw_initial_values.splitlines():
        name, value = v.split(": ")
        initial_values[name] = True if value == "1" else False

    gates = []
    for gate in raw_gates.splitlines():
        lhs, gate_type, rhs, out = re.findall(r"^(\w+) (AND|OR|XOR) (\w+) -> (\w+)", gate)[0]
        gates.append([gate_type, lhs, rhs, out])

    return initial_values, np.array(gates)


def update_wire(wire_values: dict[str, bool], gates: NDArray, wire_name: str, wire_value: bool) -> dict[str, bool]:
    wire_values[wire_name] = wire_value

    for gate_type, lhs, rhs, out in gates[(gates[:,GATE_RHS] == wire_name) | (gates[:,GATE_LHS] == wire_name)]:
        if lhs not in wire_values or rhs not in wire_values:
            continue
        vlhs = wire_values[lhs]
        vrhs = wire_values[rhs]
        if gate_type == 'AND':
            wire_values = update_wire(wire_values, gates, out, vlhs and vrhs)
        elif gate_type == 'OR':
            wire_values = update_wire(wire_values, gates, out, vlhs or vrhs)
        elif gate_type == 'XOR':
            wire_values = update_wire(wire_values, gates, out, vlhs ^ vrhs)
        else:
            raise ValueError("Invalid gate type", gate_type)

    return wire_values


def part1(input_file: str):
    initial_values, gates = get_input(input_file)
    wire_values = dict()

    for wire_name, wire_value in initial_values.items():
        wire_values = update_wire(wire_values, gates, wire_name, wire_value)

    res = "".join('1' if wire_values[k] else '0' for k in reversed(sorted(wire_values.keys())) if k.startswith("z"))
    return int(res, 2)


def part2(input_file: str):
    initial_values, gates = get_input(input_file)

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
