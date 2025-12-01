import re

PART1_SAMPLE_ANSWER = 161
PART2_SAMPLE_ANSWER = 48

MUL_PATTERN = re.compile(r"mul\((\d+),(\d+)\)")
DONT_DO_PATTERN = re.compile(r"don't\(\).*?($|do\(\))")


def get_input(file: str):
    with open(file, "r") as fd:
        return re.sub(r"\n", "", fd.read())


def perform_muls_in_string(inp: str) -> int:
    return sum(
        [
            int(match.group(1)) * int(match.group(2))
            for match in MUL_PATTERN.finditer(inp)
        ]
    )


def part1(input_file: str):
    return perform_muls_in_string(get_input(input_file))


def part2(input_file: str):
    inp = get_input(input_file)
    fixed = DONT_DO_PATTERN.sub("", inp)
    return perform_muls_in_string(fixed)


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
