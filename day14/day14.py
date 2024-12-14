import re
import itertools

from time import sleep

PART1_SAMPLE_ANSWER = 12
PART2_SAMPLE_ANSWER = 0


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    raw_dims, raw_robots = data.split("\n\n")
    w, h = map(int, re.findall(r"\d+", raw_dims))

    robots = []
    for line in raw_robots.splitlines():
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        robots.append([x, y, vx, vy])

    return (w, h, robots)


def part1(input_file: str):
    w, h, robots = get_input(input_file)

    quadrants = [0]*4
    for x, y, vx, vy in robots:
        x = (x+vx*100) % w
        y = (y+vy*100) % h

        if x < w//2 and y < h//2:
            quadrants[0] += 1
        elif x > w//2 and y < h//2:
            quadrants[1] += 1
        elif x < w//2 and y > h//2:
            quadrants[2] += 1
        elif x > w//2 and y > h//2:
            quadrants[3] += 1

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def part2(input_file: str):
    w, h, robots = get_input(input_file)

    score_history = [0]*100
    min_score = 100000000000000000
    min_score_t = 0

    input("About to run christmastree search. Press enter when ready!")

    i = 0
    while True:
        i += 1
        map = set()
        for x, y, vx, vy in robots:
            x = (x+vx*i) % w
            y = (y+vy*i) % h
            map.add((x, y))

        score = 0
        for (x1, y1), (x2, y2) in itertools.combinations(map, 2):
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            score += (dx**2 + dy**2)

        score_history = score_history[1:] + [score]
        new_min = False
        if score < min_score:
            min_score = score
            min_score_t = i
            new_min = True
            print("\x1b[H\x1b[J", end="")

        print("\r", end="")
        for s in score_history:
            BASE = 0x2581
            s = min(s // 100000000, 7)
            print(chr(BASE+s), end="")
        print(f"  {i:6} {score:10} {min_score:10} {min_score_t:6}", end="", flush=True)

        if new_min:
            print()
            for y in range(h):
                for x in range(w):
                    if (x, y) in map:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            print("\x1b[H", end="")


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
    run(part2, "input.txt")
