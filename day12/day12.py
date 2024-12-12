import numpy as np

PART1_SAMPLE_ANSWER = 1930
PART2_SAMPLE_ANSWER = 1206


def get_input(file: str):
    with open(file, "r") as fd:
        return np.array([list(row) for row in fd.read().strip().splitlines()])


def iterate_neighbors(x, y):
    yield x-1, y
    yield x+1, y
    yield x, y-1
    yield x, y+1


def get_region(map, x, y) -> tuple[set[tuple[int, int]], int, int]:
    region = set()
    h, w = map.shape
    cell = map[y, x]
    perimeter = 0
    area = 0
    def inner_loop(x, y):
        nonlocal area, perimeter
        region.update({(x, y)})
        area += 1
        for xx, yy in iterate_neighbors(x, y):
            if 0 <= xx < w and 0 <= yy < h and map[yy, xx] == cell:
                if (xx, yy) not in region:
                    inner_loop(xx, yy)
            else:
                perimeter += 1
    inner_loop(x, y)
    return region, area, perimeter


def iterate_regions(map):
    done = set()

    for y, row in enumerate(map):
        for x in range(len(row)):
            if (x, y) in done:
                continue
            region = get_region(map, x, y)
            done.update(region[0])
            yield region


def part1(input_file: str):
    map = get_input(input_file)

    res = 0
    for (_, area, peri) in iterate_regions(map):
        res += area * peri
    return res


def part2(input_file: str):
    map = get_input(input_file)
    h, w = map.shape

    res = 0

    # Create edges
    for reg, area, _ in iterate_regions(map):
        up_edges: set[tuple[int, int]] = set()
        down_edges: set[tuple[int, int]] = set()
        left_edges: set[tuple[int, int]] = set()
        right_edges: set[tuple[int, int]] = set()

        # Add edges
        for x, y in reg:
            # Up
            if y == 0 or map[y-1,x] != map[y, x]:
                up_edges.add((x, y))

            # Down
            if y == h-1 or map[y+1,x] != map[y, x]:
                down_edges.add((x, y+1))

            # Left
            if x == 0 or map[y,x-1] != map[y, x]:
                left_edges.add((x, y))

            # Right
            if x == w-1 or map[y,x+1] != map[y, x]:
                right_edges.add((x+1, y))

        # Remove repeated edges
        for x,y in list(up_edges):
            xoff = 1
            while (p := (x + xoff, y)) in up_edges:
                up_edges.remove(p)
                xoff += 1
        for x,y in list(down_edges):
            xoff = 1
            while (p := (x + xoff, y)) in down_edges:
                down_edges.remove(p)
                xoff += 1
        for x,y in list(right_edges):
            yoff = 1
            while (p := (x, y + yoff)) in right_edges:
                right_edges.remove(p)
                yoff += 1
        for x,y in list(left_edges):
            yoff = 1
            while (p := (x, y + yoff)) in left_edges:
                left_edges.remove(p)
                yoff += 1

        # Sum edges
        peri = 0
        for x, y in reg:
            if (x, y) in up_edges:
                peri += 1
            if (x, y) in left_edges:
                peri += 1
            if (x+1, y) in right_edges:
                peri += 1
            if (x, y+1) in down_edges:
                peri += 1
        res += peri * area

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
