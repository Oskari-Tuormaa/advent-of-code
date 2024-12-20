import re

import numpy as np

from dataclasses import dataclass

PART1_SAMPLE_ANSWER = 11048
PART2_SAMPLE_ANSWER = 64


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    end = (0, 0)
    start = (0, 0)
    map = []
    for y, line in enumerate(data.splitlines()):
        map.append(list(re.sub(r"S|E", ".", line)))
        for x, cell in enumerate(line):
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)

    w = len(map[0])
    h = len(map)

    return np.array(map), start, end, w, h


def iterate_ortho(x, y):
    yield x+1, y
    yield x-1, y
    yield x, y+1
    yield x, y-1


def diff_to_dir(p1: tuple[int, int], p2: tuple[int, int]) -> str:
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1

    if dx > 0 and dy == 0:
        return '>'
    if dx < 0 and dy == 0:
        return '<'
    if dx == 0 and dy > 0:
        return 'v'
    if dx == 0 and dy < 0:
        return '^'
    raise ValueError(f"Invalid points {p1=} {p2=}")


@dataclass
class Node:
    coord: tuple[int, int]
    score: int
    dir: str
    prev_node: tuple[int, int]


def astar_search(map, start, end, w, h):
    (sx, sy) = start
    (ex, ey) = end

    nodes: dict[tuple[int, int], Node] = {(sx,sy): Node((sx,sy),0,'>',(0,0))}
    open_nodes: dict[tuple[int, int], Node] = {}

    # Add starting nodes
    for x, y in iterate_ortho(sx, sy):
        if not (0 <= x < w) or not (0 <= y < h) or map[y, x] != '.':
            continue
        dir = diff_to_dir((sx, sy), (x, y))
        open_nodes[(x, y)] = Node((x, y), {'>': 1, 'v': 1001, '^': 1001, '<': 2001}[dir], dir, (sx, sy))

    # Run search
    while len(open_nodes) > 0:
        sorted_open_nodes = sorted(open_nodes.values(), key=lambda x: x.score)

        ##### Uncomment to print current map state
        # for y in range(h):
        #     for x in range(w):
        #         if (x,y) == sorted_open_nodes[0].coord:
        #             print('N', end='')
        #         elif (x,y) in open_nodes:
        #             print('?', end='')
        #         elif (x,y) in nodes:
        #             print(nodes[(x,y)].dir, end='')
        #         else:
        #             print(map[y,x], end='')
        #     print()
        # print()
        # input()

        nxt = open_nodes.pop(sorted_open_nodes[0].coord)
        nx, ny = nxt.coord

        if (nx,ny) == (ex,ey):
            nodes[(nx,ny)] = nxt
            continue

        for x, y in iterate_ortho(nx, ny):
            if not (0 <= x < w) or not (0 <= y < h) or map[y, x] != '.':
                continue

            dir = diff_to_dir((nx, ny), (x, y))
            score_from_here = nxt.score + 1 + (1000 if dir != nxt.dir else 0)

            if (x, y) in nodes:
                if score_from_here < nodes[(x,y)].score:
                    nodes[(x,y)].score = score_from_here
                    nodes[(x,y)].prev_node = (nx, ny)
                    nodes[(x,y)].dir = dir
                continue

            if (x, y) in open_nodes:
                if score_from_here < open_nodes[(x,y)].score:
                    open_nodes[(x,y)].score = score_from_here
                    open_nodes[(x,y)].prev_node = (nx, ny)
                    open_nodes[(x,y)].dir = dir
                continue

            open_nodes[(x,y)] = Node((x, y), score_from_here, dir, (nx, ny))

        nodes[(nx, ny)] = nxt

    return nodes


def part1(input_file: str):
    map, start, end, w, h = get_input(input_file)

    nodes = astar_search(map, start, end, w, h)

    return nodes[end].score


def part2(input_file: str):
    map, start, end, w, h = get_input(input_file)

    nodes = astar_search(map, start, end, w, h)

    def count_best_seats(point: tuple[int, int]):
        best_seats = set()
        cx, cy = point
        nx, ny = point

        while (cx, cy) != start:
            best_seats.add((cx, cy))
            px, py = nodes[(cx, cy)].prev_node

            if cx == nx and cy == ny:
                score_through_prev = nodes[(px,py)].score + 1
            else:
                score_through_prev = nodes[(px,py)].score + 1002 if diff_to_dir((px,py), (cx,cy)) != diff_to_dir((cx,cy),(nx,ny)) else 2

            for xx, yy in iterate_ortho(cx, cy):
                if (xx, yy) not in nodes or (xx, yy) == (px, py) or (xx, yy) == (cx, cy):
                    continue

                if cx == nx and cy == ny:
                    score_through = nodes[(xx,yy)].score + 1
                else:
                    score_through = nodes[(xx,yy)].score + (1002 if diff_to_dir((xx,yy), (cx,cy)) != diff_to_dir((cx,cy),(nx,ny)) else 2)

                if score_through_prev == score_through:
                    best_seats.update(count_best_seats((xx, yy)))

            nx, ny = cx, cy
            cx, cy = px, py
        return best_seats

    return len(count_best_seats(end)) + 1


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
