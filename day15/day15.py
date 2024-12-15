from dataclasses import dataclass


PART1_SAMPLE_ANSWER = 10092
PART2_SAMPLE_ANSWER = 9021


@dataclass
class Map:
    walls: set[tuple[int, int]]
    boxes: set[tuple[int, int]]
    robot_position: tuple[int, int]


DIRS = {
    '^': ( 0, -1),
    'v': ( 0,  1),
    '>': ( 1,  0),
    '<': (-1,  0),
}


def get_input(file: str):
    with open(file, "r") as fd:
        data = fd.read().strip()

    raw_map, moves = data.split("\n\n")
    moves = moves.replace('\n', '')

    walls = set()
    boxes = set()
    robot_position = (0, 0)
    for y, row in enumerate(raw_map.splitlines()):
        for x, cell in enumerate(row):
            if cell == '#':
                walls.add((x, y))
            elif cell == 'O':
                boxes.add((x, y))
            elif cell == '@':
                robot_position = (x, y)

    return Map(walls, boxes, robot_position), moves


def perform_move(map: Map, move: str) -> Map:
    dx, dy = DIRS[move]
    rx, ry = map.robot_position
    x, y = rx, ry

    x += dx
    y += dy

    box_to_move = None
    while (x, y) in map.boxes:
        box_to_move = (x, y)
        x += dx
        y += dy

    if (x, y) in map.walls:
        return map

    new_robot_pos = (rx+dx, ry+dy)
    if box_to_move is not None:
        map.boxes.remove(new_robot_pos)
        bx, by = box_to_move
        map.boxes.add((bx+dx, by+dy))

    map.robot_position = new_robot_pos

    return map


def part1(input_file: str):
    map, moves = get_input(input_file)

    for move in moves:
        map = perform_move(map, move)

    res = 0
    for (bx, by) in map.boxes:
        res += bx + 100 * by

    return res


def widen_map(map: Map) -> Map:
    walls = set()
    boxes = set()

    for (wx, wy) in map.walls:
        walls.add((wx*2, wy))
        walls.add((wx*2+1, wy))

    for (bx, by) in map.boxes:
        boxes.add((bx*2, by))

    rx, ry = map.robot_position
    robot_position = (rx*2, ry)

    return Map(walls, boxes, robot_position)


def perform_wide_move(map: Map, move: str) -> Map:
    rx, ry = map.robot_position
    dx, dy = DIRS[move]

    to_move = set()
    to_check = {(rx+dx, ry+dy)}
    while len(to_check) != 0:
        x, y = to_check.pop()

        if (x, y) in map.walls:
            return map

        if (hit_lhs := (x, y) in map.boxes) or (x-1, y) in map.boxes:
            bx, by = x if hit_lhs else x-1, y

            to_move.add((bx, by))
            if dx == 0:
                to_check.add((bx, by+dy))
                to_check.add((bx+1, by+dy))
            elif move == '<':
                to_check.add((bx-1, by))
            elif move == '>':
                to_check.add((bx+2, by))

    moved_set = {(bx+dx, by+dy) for bx,by in to_move}
    for (bx, by) in to_move:
        map.boxes.remove((bx, by))
    for box in moved_set:
        map.boxes.add(box)

    map.robot_position = (rx+dx, ry+dy)

    return map


def part2(input_file: str):
    map, moves = get_input(input_file)
    map = widen_map(map)
    
    for move in moves:
        map = perform_wide_move(map, move)

    res = 0
    for (bx, by) in map.boxes:
        res += bx + 100 * by

    return res


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
