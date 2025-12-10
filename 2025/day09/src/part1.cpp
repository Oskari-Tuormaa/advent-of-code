#include "parse.hpp"

#include <cstdlib>
#include <print>
#include <ranges>

void part1(ParseType d)
{
    long largest = 0;

    for (auto [i, p1] : d | std::views::enumerate) {
        auto [x1, y1] = p1;
        for (auto [x2, y2] : d | std::views::drop(i + 1)) {
            auto dx = std::abs(x2 - x1) + 1;
            auto dy = std::abs(y2 - y1) + 1;
            largest = std::max(largest, dx * dy);
        }
    }

    std::println("{}", largest);
}
