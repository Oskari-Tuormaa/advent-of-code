import numpy as np

from numpy.typing import NDArray
from typing import Generator

PART1_SAMPLE_ANSWER = 1928
PART2_SAMPLE_ANSWER = 2858


def get_input(file: str):
    with open(file, "r") as fd:
        return [int(x) for x in fd.read().strip()]


def yield_files(map: list[int]) -> Generator[int | None, None, None]:
    for i, n in enumerate(map):
        for _ in range(n):
            if i % 2 == 0:
                yield i // 2
            else:
                yield None

def part1(input_file: str):
    map = get_input(input_file)

    backward_it = reversed(list(enumerate(yield_files(map))))
    def get_next_backward() -> tuple[int, int]:
        while True:
            ni, nv = next(backward_it)
            if nv is not None:
                return ni, nv

    bi = 100000000
    res = 0
    for i, v in enumerate(yield_files(map)):
        if i == bi:
            break
        if v is None:
            bi, bv = get_next_backward()
            res += i * bv
        else:
            res += i * v

    return res


# File contents: FileID, FileSize, EmptySize, PrevIdx, NxtIdx
FILE_ID = 0
FILE_SIZE = 1
EMPTY_SIZE = 2
PREV_IDX = 3
NXT_IDX = 4
def map_to_files(map: list[int]) -> NDArray:
    n_files = len(map)//2
    files = np.array([[0, 0, 0, 0, 0]]*n_files)
    for file_id, (file_size, empty_size) in enumerate(zip(map[::2], map[1::2])):
        nxt_idx = file_id + 1
        prev_idx = file_id - 1
        if file_id == 0:
            prev_idx = -1
        elif file_id == n_files-1:
            nxt_idx = -1
        files[file_id] = [file_id, file_size, empty_size, prev_idx, nxt_idx]
    return files


def iterate_files(files: NDArray) -> Generator[NDArray, None, None]:
    nxt_file = files[files[:,PREV_IDX] == -1][0]
    while nxt_file[NXT_IDX] != -1:
        yield nxt_file
        nxt_file = files[nxt_file[NXT_IDX]]
    yield nxt_file


def defrag(files: NDArray) -> NDArray:
    n_files = len(files)

    for fid in range(n_files-1, -1, -1):
        _, fsz, esz, pi, ni = files[fid]

        # Iterate through files
        for file in iterate_files(files):
            ffid, _, eesz, _, nni = file
            if ffid == fid:
                break
            if fsz > eesz:
                continue

            # Special case: File is only shifted, but neighbors are the same
            if ffid == pi:
                files[fid][EMPTY_SIZE] += files[pi][EMPTY_SIZE]
                files[pi][EMPTY_SIZE] = 0
                break

            # Update original previous file
            files[pi][EMPTY_SIZE] += fsz+esz
            files[pi][NXT_IDX] = ni

            # Update original next file
            if ni != -1:
                files[ni][PREV_IDX] = pi

            # Update self
            files[fid][PREV_IDX] = ffid
            files[fid][NXT_IDX] = nni
            files[fid][EMPTY_SIZE] = eesz - fsz

            # Update new next file
            files[nni][PREV_IDX] = fid

            # Update new previous file
            files[ffid][NXT_IDX] = fid
            files[ffid][EMPTY_SIZE] = 0
            break

    return files


def part2(input_file: str):
    map = get_input(input_file)
    map += [0]

    files = map_to_files(map)
    files = defrag(files)

    i = 0
    res = 0
    for file2 in iterate_files(files):
        fid2, fsz2, esz2, _, _ = file2
        for _ in range(fsz2):
            res += fid2 * i
            i += 1
        i += esz2

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
