import itertools
import re

from typing import Generator

PART1_SAMPLE_ANSWER = 126384
PART2_SAMPLE_ANSWER = 0


coord = tuple[int, int]


KEYPAD = {
    '0': (1,0),
    'A': (2,0),
    '1': (0,1),
    '2': (1,1),
    '3': (2,1),
    '4': (0,2),
    '5': (1,2),
    '6': (2,2),
    '7': (0,3),
    '8': (1,3),
    '9': (2,3),
}

RKEYPAD = {
    (1,0): '0',
    (2,0): 'A',
    (0,1): '1',
    (1,1): '2',
    (2,1): '3',
    (0,2): '4',
    (1,2): '5',
    (2,2): '6',
    (0,3): '7',
    (1,3): '8',
    (2,3): '9',
}

DPAD = {
    '<': (0,0),
    'v': (1,0),
    '>': (2,0),
    '^': (1,1),
    'A': (2,1),
}

RDPAD = {
    (0,0): '<',
    (1,0): 'v',
    (2,0): '>',
    (1,1): '^',
    (2,1): 'A',
}


SGN_X = {
    -1: '<',
    0: '',
    1: '>'
}

SGN_Y = {
    -1: 'v',
    0: '',
    1: '^'
}


def get_input(file: str):
    with open(file, "r") as fd:
        return fd.read().strip().splitlines()


def sign(v):
    return v/abs(v) if v != 0 else 0


def path_to(pad: dict[str, coord], frm: str, to: str) -> str:
    fromx, fromy = pad[frm]
    tox, toy = pad[to]

    dx = tox - fromx
    dy = toy - fromy

    chx = SGN_X[int(sign(dx))]
    chy = SGN_Y[int(sign(dy))]

    if (tox, fromy) not in pad.values():
        return chy*abs(dy) + chx*abs(dx)
    else:
        return chx*abs(dx) + chy*abs(dy)


def press_buttons(pad: dict[str, coord], path: str) -> str:
    res = ""
    for f, t in itertools.pairwise(path):
        res += path_to(pad, f, t) + 'A'
    return res


def yield_path_to(pad: dict[str, coord], frm: str, to: str) -> Generator[str, None, None]:
    fromx, fromy = pad[frm]
    tox, toy = pad[to]

    dx = tox - fromx
    dy = toy - fromy

    chx = SGN_X[int(sign(dx))]
    chy = SGN_Y[int(sign(dy))]

    if dx == 0 or dy == 0:
        yield chx*abs(dx) + chy*abs(dy)
        return

    if (tox, fromy) in pad.values():
        yield chx*abs(dx) + chy*abs(dy)
    if (fromx, toy) in pad.values():
        yield chy*abs(dy) + chx*abs(dx)


def yield_press_buttons(pad: dict[str, coord], path: str) -> Generator[str, None, None]:
    def yield_next(pad, path):
        if len(path) < 2:
            yield ''
            return
        for p in yield_path_to(pad, path[0], path[1]):
            for n in yield_next(pad, path[1:]):
                yield p+'A'+n
    yield from yield_next(pad, path)


def extract_number(v: str) -> int:
    return int("".join(re.findall(r"\d+", v)))


DPAD_DRAW = """
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""

KEYPAD_DRAW = """
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

def visualize_presses(sequence: str):
    pos = [
        DPAD['A'],
        DPAD['A'],
        KEYPAD['A'],
    ]

    delta = {
        '>': (1, 0),
        '<': (-1, 0),
        'v': (0, -1),
        '^': (0, 1),
    }

    code = ''

    def perform_press(ch: str, pos: list[coord]) -> list[coord]:
        nonlocal code
        if ch == 'A':
            if len(pos) > 1:
                return [pos[0]] + perform_press(RDPAD[pos[0]], pos[1:])
            # code += RKEYPAD[pos[0]]
            return pos
        dx, dy = delta[ch]
        px, py = pos[0]
        pos[0] = (px+dx, py+dy)
        return pos

    for i, p in enumerate(sequence):
        print(sequence[:i])
        print(code)
        print(DPAD_DRAW.replace(RDPAD[pos[0]],   '\x1b[31m#\x1b[0m'))
        print(DPAD_DRAW.replace(RDPAD[pos[1]],   '\x1b[31m#\x1b[0m'))
        # print(KEYPAD_DRAW.replace(RKEYPAD[pos[2]], '\x1b[31m#\x1b[0m'))
        input()
        pos = perform_press(p, pos)


def part1(input_file: str):
    codes = get_input(input_file)

    res = 0
    for code in codes:
        r1 = [r for r in yield_press_buttons(KEYPAD, 'A'+code)]
        r2 = [r for rr in r1 for r in yield_press_buttons(DPAD, 'A'+rr)]
        r3 = [r for rr in r2 for r in yield_press_buttons(DPAD, 'A'+rr)]
        best = min(r3, key=lambda x: len(x))
        res += len(best) * extract_number(code)

    return res


def part2(input_file: str):
    codes = get_input(input_file)

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
