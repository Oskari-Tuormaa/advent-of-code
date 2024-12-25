from typing import Generator
from numba import njit


PART1_SAMPLE_ANSWER = 44
PART2_SAMPLE_ANSWER = 285


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    start = (0,0)
    end = (0,0)
    walls = set()
    lines = data.splitlines()
    w = len(lines[0])
    h = len(lines)
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == 'S':
                start = (x,y)
            elif cell == 'E':
                end = (x,y)
            elif cell == '#':
                walls.add((x,y))

    return start, end, w, h, walls


Coord = tuple[int, int]
@njit
def neighbors(x: int, y: int) -> Generator[Coord, None, None]:
    yield x,y
    yield x-1,y
    yield x+1,y
    yield x,y-1
    yield x,y+1


@njit
def neighbors_in(x: int, y: int, w: int, h: int) -> Generator[Coord, None, None]:
    for xx,yy in neighbors(x,y):
        if 0 <= xx < w and 0 <= yy < h:
            yield xx,yy


def generate_path(start: Coord, end: Coord, w: int, h: int, walls: set[Coord]) -> dict[Coord, int]:
    x, y = start
    path = dict()
    ps = 0
    while True:
        path[(x,y)] = ps
        ps += 1
        if (x,y) == end:
            break
        for xx,yy in neighbors_in(x, y, w, h):
            if (xx,yy) not in path and (xx,yy) not in walls:
                x,y = xx,yy
    return path


def manhattan(x1: int, y1: int, x2: int, y2: int):
    return abs(x2-x1) + abs(y2-y1)


def yield_in_distance(w: int, h: int, point: Coord, distance: int) -> Generator[Coord, None, None]:
    px, py = point

    xfrom = max(0, px - distance)
    xto   = min(w-1, px + distance)+1
    yfrom = max(0, py - distance)
    yto   = min(h-1, py + distance)+1

    for y in range(yfrom, yto):
        for x in range(xfrom, xto):
            yield (x,y)


def get_cheats(path: dict[Coord, int], w: int, h: int, minimum_save: int, maximum_cheat: int) -> dict[int, int]:
    done = set()
    cheats = dict()

    for p1 in path:
        for p2 in yield_in_distance(w, h, p1, maximum_cheat):
            if p2 not in path or path[p2] <= path[p1] or (p1, p2) in done:
                continue

            d = manhattan(*p1, *p2)
            if not (0 < d <= maximum_cheat):
                continue

            save = path[p2] - path[p1] - d
            if save < minimum_save:
                continue

            if save not in cheats:
                cheats[save] = 0
            cheats[save] += 1
            done.add((p1,p2))

    return cheats


def part1(input_file: str, minimum_saved: int):
    start, end, w, h, walls = get_input(input_file)
    path = generate_path(start, end, w, h, walls)
    counts = get_cheats(path, w, h, minimum_saved, 2)
    return sum(counts.values())


def part2(input_file: str, minimum_saved: int):
    start, end, w, h, walls = get_input(input_file)
    path = generate_path(start, end, w, h, walls)
    counts = get_cheats(path, w, h, minimum_saved, 20)
    return sum(counts.values())


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
    sol, dt = run(part1, "sample.txt", 1)
    print(f"Part 1 -- Sample [{dt:9.5f}s]: {sol}")
    assert sol == PART1_SAMPLE_ANSWER, f"{sol} != {PART1_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part1, "input.txt", 100)
    print(f"Part 1 --- Input [{dt:9.5f}s]: {sol}")

    print()
    sol, dt = run(part2, "sample.txt", 50)
    print(f"Part 2 -- Sample [{dt:9.5f}s]: {sol}")
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, "input.txt", 100)
    print(f"Part 2 --- Input [{dt:9.5f}s]: {sol}")
