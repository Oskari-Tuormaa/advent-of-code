from itertools import combinations, product, chain
from typing import Generator

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
def neighbors(x: int, y: int) -> Generator[Coord, None, None]:
    yield x-1,y
    yield x+1,y
    yield x,y-1
    yield x,y+1


def neighbors_in(x: int, y: int, w: int, h: int) -> Generator[Coord, None, None]:
    yield from [
        (xx,yy) for xx,yy in neighbors(x,y)
        if 0 <= xx < w and 0 <= yy < h
    ]


def print_map(w: int, h: int, walls: set[Coord], s: Coord, e: Coord, c1: Coord, c2: Coord):
    chars = {p:(37, '#') for p in walls}
    chars.update({
        s:  (31, 'S'),
        e:  (32, 'E'),
        c1: (33, '1'),
        c2: (34, '2'),
    })
    for y in range(h):
        for x in range(w):
            p = (x,y)
            if p in chars:
                col, ch = chars[p]
                print(f'\x1b[{col}m{ch}\x1b[0m', end='')
            else:
                print('.', end='')
        print()


def generate_path(start: Coord, end: Coord, w: int, h: int, walls: set[Coord]) -> tuple[set[Coord], dict[Coord, int]]:
    x, y = start
    path_adjacent_walls = set()
    path = dict()
    ps = 0
    while True:
        path[(x,y)] = ps
        ps += 1
        if (x,y) == end:
            break
        for xx,yy in neighbors_in(x, y, w, h):
            if (xx,yy) in walls:
                path_adjacent_walls.add((xx,yy))
            elif (xx,yy) not in path:
                x,y = xx,yy
    return path_adjacent_walls, path


def manhattan(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)


def part1(input_file: str, minimum_saved: int):
    start, end, w, h, walls = get_input(input_file)
    path_adjacent_walls, path = generate_path(start, end, w, h, walls)

    adjacent_times  = lambda x,y: list(path[(xx,yy)] for xx,yy in neighbors_in(x,y,w,h) if (xx,yy) in path)

    def latest_time_for(x: int, y: int) -> int | None:
        times = adjacent_times(x, y) + [path[(x,y)]] if (x,y) in path else []
        if len(times) > 0:
            return max(times)

    cheats = set()
    cheat_count = dict()
    for wx,wy in path_adjacent_walls:
        earliest_time = min(adjacent_times(wx, wy))
        for xx,yy in neighbors_in(wx, wy, w, h):
            if (latest_time := latest_time_for(xx, yy)) is None:
                continue

            t_save = latest_time - earliest_time - 3
            if (xx,yy) == end:
                t_save += 1

            if t_save < minimum_saved:
                continue

            if t_save not in cheat_count:
                cheat_count[t_save] = 0
            cheat_count[t_save] += 1

            cheats.add(((wx,wy),(xx,yy),t_save))
            # print(f'{earliest_time=:3}  --  {latest_time=:3} -- {t_save=:3} -- {cheat_count=}')
            # print_map(w, h, walls, start, end, (wx,wy), (xx,yy))
            # input()

    save_times = [t for _,_,t in cheats]
    save_times = {t:save_times.count(t) for t in {tt for tt in save_times}}

    # for k in sorted(save_times.keys()):
    #     print(f"{k:3}: {save_times[k]:3}")

    return len(cheats)


def calc_save(path: dict[Coord, int], w: int, h: int, c1: Coord, c2: Coord) -> int:
    x1, y1 = c1
    x2, y2 = c2

    d = manhattan(x1, y1, x2, y2)

    adjacent_on_path1 = list((xx,yy,path[xx,yy]) for xx,yy in [*neighbors_in(x1, y1, w, h),(x1,y1)] if (xx,yy) in path)
    adjacent_on_path2 = list((xx,yy,path[xx,yy]) for xx,yy in [*neighbors_in(x2, y2, w, h),(x2,y2)] if (xx,yy) in path)

    px1, py1, t1 = min(adjacent_on_path1, key=lambda x: x[2])
    px2, py2, t2 = max(adjacent_on_path2, key=lambda x: x[2])

    return t2 - t1 - d - sum([(px1,py1) != c1, (px2,py2) != c2])


def part2(input_file: str, minimum_saved: int):
    start, end, w, h, walls = get_input(input_file)
    path_adjacent_walls, path = generate_path(start, end, w, h, walls)

    to_check = chain(combinations(path_adjacent_walls, 2), product(path_adjacent_walls, path))
    cheats = dict()
    for p1, p2 in to_check:
        d = manhattan(*p1, *p2) + 1
        if d > 2:
            continue

        save = calc_save(path, w, h, p1, p2)
        if save < 0:
            continue
        if save not in cheats:
            cheats[save] = 0
        cheats[save] += 1

    for k in sorted(cheats.keys()):
        print(f"{k:3}: {cheats[k]:3}")

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
