#include "parse.hpp"

#include <print>
#include <span>

bool in_range(Range r, long num)
{
    return num >= r.start && num <= r.end;
}

bool is_in_any_range(std::span<Range> ranges, long num)
{
    for (auto r : ranges) {
        if (in_range(r, num)) {
            return true;
        }
    }
    return false;
}

void part1(ParseType d)
{
    int res                     = 0;
    auto& [ranges, ingredients] = d;

    for (auto i : ingredients) {
        if (is_in_any_range(ranges, i)) {
            res++;
        }
    }

    std::println("{}", res);
}
