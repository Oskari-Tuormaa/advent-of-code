import re

from dataclasses import dataclass

PART1_SAMPLE_ANSWER = 22
PART2_SAMPLE_ANSWER = 6,1


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    raw_dims, raw_bytes = data.split("\n\n")
    w, h = map(int, re.findall(r'\d+', raw_dims))

    byts: list[tuple[int, int]] = []
    for line in raw_bytes.splitlines():
        x, y = map(int, re.findall(r'\d+', line))
        byts.append((x, y))

    return w, h, byts


def neighbors(x, y):
    yield x-1, y
    yield x+1, y
    yield x, y-1
    yield x, y+1


def neighbors_in(x, y, w, h):
    yield from [
        (xx, yy) for xx,yy in neighbors(x,y)
        if 0 <= xx < w and 0 <= yy < h
    ]


@dataclass
class Node:
    coords: tuple[int, int]
    score: int
    prev_node: tuple[int, int] | None


def astar(start: tuple[int, int], end: tuple[int, int], w: int, h: int, obstacles: set[tuple[int, int]]):
    nodes: dict[tuple[int, int], Node] = {start: Node(start, 0, None)}
    open_nodes: dict[tuple[int, int], Node] = {}

    sx, sy = start
    ex, ey = end

    for x, y in neighbors_in(sx, sy, w, h):
        if (x,y) in obstacles:
            continue
        open_nodes[x,y] = Node((x,y), 1, (sx, sy))

    while len(open_nodes) > 0:
        sorted_nodes = sorted(open_nodes.values(), key=lambda x: x.score)

        nxt_node = open_nodes.pop(sorted_nodes[0].coords)
        nx, ny = nxt_node.coords
        nodes[nx,ny] = nxt_node

        if (nx,ny) == (ex,ey):
            nodes[nx,ny] = nxt_node
            return nodes

        for x,y in neighbors_in(nx, ny, w, h):
            if (x,y) in obstacles:
                continue

            n_score = nxt_node.score + 1

            if (x,y) in nodes:
                if n_score < nodes[x,y].score:
                    nodes[x,y].score = n_score
                    nodes[x,y].prev_node = nx,ny
                continue

            if (x,y) in open_nodes:
                if n_score < open_nodes[x,y].score:
                    open_nodes[x,y].score = n_score
                    open_nodes[x,y].prev_node = nx,ny
                continue

            open_nodes[x,y] = Node((x,y), n_score, (nx,ny))

    return nodes


def traverse_reversed(nodes: dict[tuple[int, int], Node], start: tuple[int, int]):
    x, y = start
    while (nxt := nodes[x,y].prev_node) is not None:
        yield x,y
        x,y = nxt
    yield nxt


def part1(input_file: str, n_fallen: int):
    w, h, byts = get_input(input_file)
    start = (0,0)
    end = (w-1,h-1)

    nodes = astar(start, end, w, h, set(byts[:n_fallen]))
    path = list(traverse_reversed(nodes, (w-1,h-1)))

    return len(path) - 1


def part2(input_file: str):
    w, h, byts = get_input(input_file)

    start = (0,0)
    end = (w-1,h-1)

    nodes = astar(start, end, w, h, set())
    current_path = list(traverse_reversed(nodes, end))

    for i in range(len(byts)):
        nx,ny = byts[i-1]
        if (nx,ny) not in current_path:
            continue

        nodes = astar(start, end, w, h, set(byts[:i]))
        if end not in nodes:
            return byts[i-1]
        current_path = list(traverse_reversed(nodes, end))


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
    sol, dt = run(part1, "sample.txt", 12)
    print(f"Part 1 -- Sample [{dt:9.5f}s]: {sol}")
    assert sol == PART1_SAMPLE_ANSWER, f"{sol} != {PART1_SAMPLE_ANSWER}"

    # with nostdout():
    sol, dt = run(part1, "input.txt", 1024)
    print(f"Part 1 --- Input [{dt:9.5f}s]: {sol}")

    print()
    sol, dt = run(part2, "sample.txt")
    print(f"Part 2 -- Sample [{dt:9.5f}s]: {sol}")
    assert sol == PART2_SAMPLE_ANSWER, f"{sol} != {PART2_SAMPLE_ANSWER}"

    with nostdout():
        sol, dt = run(part2, "input.txt")
    print(f"Part 2 --- Input [{dt:9.5f}s]: {sol}")
