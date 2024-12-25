from itertools import combinations
from typing import Generator

PART1_SAMPLE_ANSWER = 7
PART2_SAMPLE_ANSWER = "co,de,ka,ta"


def get_input(file: str):
    with open(file, "r") as fd:
        data = list(l.split('-') for l in fd.read().strip().splitlines())

    computers = dict()
    for lhs, rhs in data:
        if lhs not in computers:
            computers[lhs] = set()
        if rhs not in computers:
            computers[rhs] = set()
        computers[lhs].add(rhs)
        computers[rhs].add(lhs)
    return computers


def yield_connected(connections: dict[str, set[str]], size: int) -> Generator[set[str], None, None]:
    done = []
    for comp, conn in connections.items():
        for to_check in combinations(conn, size-1):
            if any(c1 not in connections[c2] for c1,c2 in combinations(to_check, 2)) or {comp, *to_check} in done:
                continue
            done.append({comp, *to_check})
            yield {comp, *to_check}


def find_largest_connection(connections: dict[str, set[str]]) -> set[str]:
    size = max(len(conn) for conn in connections.values())

    while size > 1:
        try:
            return next(yield_connected(connections, size))
        except StopIteration:
            size -= 1

    return set()


def part1(input_file: str):
    connections = get_input(input_file)
    return sum(1 for trio in yield_connected(connections, 3) if any(comp.startswith('t') for comp in trio))


def part2(input_file: str):
    connections = get_input(input_file)
    largest_set = find_largest_connection(connections)
    return ",".join(sorted(largest_set))


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
