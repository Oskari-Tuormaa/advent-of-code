#include "parse.hpp"

#include <print>

void part2(ParseType d) {
    int res  = 0;
    int dial = 50;

    for (auto [dir, len] : d) {
        for (int i = 0; i < len; i++) {
            dial = (dir == Dir::Right ? dial + 1 : dial - 1) % 100;
            if (dial == 0)
                res++;
        }
    }

    std::println("{}", res);
}
