Rule = set[int]
Rules = dict[int, Rule]
Update = list[int]
Updates = list[Update]


def get_input(file: str):
    with open(file, "r") as fd:
        return fd.read()


def parse_rules(inp: str) -> Rules:
    rules: dict[int, set[int]] = dict()

    for lhs, rhs in [line.split("|") for line in inp.split("\n")]:
        lhs, rhs = int(lhs), int(rhs)
        if lhs not in rules:
            rules[lhs] = set()
        rules[lhs].add(rhs)

    return rules


def is_update_corect(rules: Rules, update: Update) -> bool:
    for i, num in enumerate(update):
        if num in rules and any(n in rules[num] for n in update[:i]):
            return False
    return True


def yield_correct_updates(rules: Rules, updates: Updates):
    for update in updates:
        if is_update_corect(rules, update):
            yield update


def yield_incorrect_updates(rules: Rules, updates: Updates):
    for update in updates:
        for i, num in enumerate(update):
            if num in rules and any(r in update[:i] for r in rules[num]):
                yield update
                break


def fix_update(rules: Rules, update: Update) -> Update:
    def perform_single_fix() -> bool:
        for i, num in enumerate(update):
            if num not in rules:
                continue

            for j, nnum in enumerate(update[:i]):
                if nnum in rules[num]:
                    tmp = update[j]
                    update[j] = update[i]
                    update[i] = tmp
                    return False
        return True

    while not perform_single_fix():
        pass

    return update


def part1(input_file: str):
    inp = get_input(input_file)

    raw_rules, raw_updates = inp.split("\n\n")

    rules = parse_rules(raw_rules)
    updates = list(list(map(int, line.split(','))) for line in raw_updates.split('\n')[:-1])

    res = 0
    for update in yield_correct_updates(rules, updates):
        res += update[len(update)//2]

    return res


def part2(input_file: str):
    inp = get_input(input_file)

    raw_rules, raw_updates = inp.split("\n\n")

    rules = parse_rules(raw_rules)
    updates = list(list(map(int, line.split(','))) for line in raw_updates.split('\n')[:-1])

    res = 0
    for update in yield_incorrect_updates(rules, updates):
        fixed_update = fix_update(rules, update)
        res += fixed_update[len(fixed_update)//2]

    return res


if __name__ == "__main__":
    print("Part 1 -- Sample:", part1("sample.txt"))
    print("Part 1 --- Input:", part1("input.txt"))

    print()
    print("Part 2 -- Sample:", part2("sample.txt"))
    print("Part 2 --- Input:", part2("input.txt"))
