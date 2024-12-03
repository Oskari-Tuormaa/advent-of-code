import re

MUL_PATTERN = re.compile(r"mul\((\d+),(\d+)\)")
DONT_DO_PATTERN = re.compile(r"don't\(\).*?($|do\(\))")


def get_input(file: str):
    with open(file, "r") as fd:
        return re.sub(r"\n", "", fd.read())


def perform_muls_in_string(inp: str) -> int:
    return sum(
        [
            int(match.group(1)) * int(match.group(2))
            for match in MUL_PATTERN.finditer(inp)
        ]
    )


def part1(input_file: str):
    return perform_muls_in_string(get_input(input_file))


def part2(input_file: str):
    inp = get_input(input_file)
    fixed = DONT_DO_PATTERN.sub("", inp)
    return perform_muls_in_string(fixed)


if __name__ == "__main__":
    print("Part 1 -- Sample:", part1("sample1.txt"))
    print("Part 1 --- Input:", part1("input.txt"))

    print()
    print("Part 2 -- Sample:", part2("sample2.txt"))
    print("Part 2 --- Input:", part2("input.txt"))
