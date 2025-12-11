#include "parse.hpp"

#include <print>

long traverse_devices(const ParseType& d, Name current)
{
    long res { 0 };

    if (current == out) {
        return 1;
    }

    for (auto n : d.at(current)) {
        res += traverse_devices(d, n);
    }

    return res;
}

void part1(ParseType d)
{
    std::println("{}", traverse_devices(d, you));
}
