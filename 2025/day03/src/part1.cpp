#include "common.hpp"
#include "parse.hpp"

#include <print>

void part1(ParseType d)
{
    std::println("{}", total_joltage(d, [](Pack pack) { return largest_joltage(pack, 2); }));
}
