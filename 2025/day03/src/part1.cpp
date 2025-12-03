#include "common.hpp"
#include "input.hpp"

#include <algorithm>
#include <print>

// #define DEBUG

long largest_joltage(Pack pack)
{
    int  max     = std::ranges::max(pack.subspan(0, pack.size() - 1));
    auto max_pos = std::ranges::find(pack, max);
    int  nxt     = std::ranges::max(Pack { max_pos + 1, pack.end() });

#ifdef DEBUG
    std::println("{} -> {} {}", pack, max, nxt);
#endif
    return max * 10 + nxt;
}

void part1()
{
    std::println("test input: {}", total_joltage(test_input, largest_joltage));
    std::println("real input: {}", total_joltage(real_input, largest_joltage));
}
