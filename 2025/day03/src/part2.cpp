#include "common.hpp"
#include "input.hpp"

#include <algorithm>
#include <cmath>
#include <print>

// #define DEBUG

long largest_joltage(Pack pack, int n_batteries)
{
    if (n_batteries == 0) {
        return 0;
    }

    int  max     = std::ranges::max(pack.subspan(0, pack.size() - n_batteries + 1));
    auto max_pos = std::ranges::find(pack, max);

#ifdef DEBUG
    std::println("{} -> {}", pack, max);
#endif

    return max * std::pow(10, n_batteries - 1)
        + largest_joltage(Pack { max_pos + 1, pack.end() }, n_batteries - 1);
}

long largest_joltage_12(Pack pack)
{
    long joltage = largest_joltage(pack, 12);
    return joltage;
}

void part2()
{
    std::println("test input: {}", total_joltage(test_input, largest_joltage_12));
    std::println("real input: {}", total_joltage(real_input, largest_joltage_12));
}
