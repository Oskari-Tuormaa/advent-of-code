#include "parse.hpp"

#include <print>

void part1(ParseType d) {
    int res  = 0;
    int dial = 50;

    for (auto [dir, len] : d) {
        dial = (dir == Dir::Left ? dial + len : dial - len) % 100;
        if (dial == 0)
            res++;
    }

    std::println("{}", res);
}
