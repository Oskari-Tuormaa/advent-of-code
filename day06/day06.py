from enum import Enum
from typing import Generator

PART1_SAMPLE_ANSWER = 41
PART2_SAMPLE_ANSWER = 6


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def rot90(self) -> "Direction":
        if self == Direction.UP:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.LEFT
        elif self == Direction.LEFT:
            return Direction.UP
        raise ValueError("Invalid direction", self)

    def to_delta(self) -> tuple[int, int]:
        if self == Direction.UP:
            return (0, -1)
        elif self == Direction.RIGHT:
            return (1, 0)
        elif self == Direction.DOWN:
            return (0, 1)
        elif self == Direction.LEFT:
            return (-1, 0)
        raise ValueError("Invalid direction", self)

    def step(self, position: tuple[int, int]) -> tuple[int, int]:
        x, y = position
        dx, dy = self.to_delta()
        return (x + dx, y + dy)


def get_input(file: str):
    with open(file, "r") as fd:
        lines = fd.readlines()

    obstacles: set[tuple[int, int]] = set()
    map_dimensions: tuple[int, int] = (len(lines[0][:-1]), len(lines))
    starting_pos: tuple[int, int] = (0, 0)
    for y, line in enumerate(lines):
        for x, cell in enumerate(line[:-1]):
            if cell == "#":
                obstacles.add((x, y))
            elif cell == "^":
                starting_pos = (x, y)
    return obstacles, map_dimensions, starting_pos


def is_within_map(pos: tuple[int, int], dim: tuple[int, int]) -> bool:
    x, y = pos
    w, h = dim
    if x < 0 or y < 0 or x >= w or y >= h:
        return False
    return True


def walk_along_path(
    obstacles: set[tuple[int, int]],
    map_dimensions: tuple[int, int],
    starting_pos: tuple[int, int],
    direction: Direction = Direction.UP,
) -> Generator[tuple[tuple[int, int], Direction], None, None]:
    pos = starting_pos
    dir = direction
    yield pos, dir
    while is_within_map(pos, map_dimensions):
        nxtPos = dir.step(pos)
        if nxtPos in obstacles:
            dir = dir.rot90()
        else:
            pos = nxtPos
        if is_within_map(pos, map_dimensions):
            yield pos, dir


def part1(input_file: str):
    obstacles, map_dimensions, starting_pos = get_input(input_file)

    visited = set()
    for node, _ in walk_along_path(obstacles, map_dimensions, starting_pos):
        visited.add(node)

    return len(visited)


def part2(input_file: str):
    obstacles, map_dimensions, starting_pos = get_input(input_file)

    loops = set()
    has_visited = set()
    for node, dir in walk_along_path(obstacles, map_dimensions, starting_pos):

        obstacle_pos = dir.step(node)
        if (
            obstacle_pos not in obstacles
            and obstacle_pos not in has_visited
            and obstacle_pos != starting_pos
        ):

            visited = set()
            for n2 in walk_along_path(
                {*obstacles, obstacle_pos}, map_dimensions, node, dir.rot90()
            ):
                if n2 in visited:
                    loops.add(obstacle_pos)
                    break
                visited.add(n2)

        has_visited.add(node)

    return len(loops)


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
