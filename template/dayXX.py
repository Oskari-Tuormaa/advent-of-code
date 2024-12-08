PART1_SAMPLE_ANSWER = 0
PART2_SAMPLE_ANSWER = 0


def get_input(file: str):
    with open(file, "r") as fd:
        return fd.read()


def part1(input_file: str):
    inp = get_input(input_file)
    return 0


def part2(input_file: str):
    inp = get_input(input_file)
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