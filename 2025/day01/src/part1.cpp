#include "ansi.hpp"
#include "input.hpp"

#include <print>

int calculate_password(std::span<const Move> moves)
{
    int res  = 0;
    int dial = 50;

    for (auto [dir, len] : moves) {
        dial = (dir == Dir::LEFT ? dial + len : dial - len) % 100;
        if (dial == 0)
            res++;
    }

    return res;
}

void part1()
{
    std::println(PURPLE "### Part 1 ###" RESET);
    int res;

    res = calculate_password(test_input);
    std::println("Result test: {}", res);

    res = calculate_password(real_input);
    std::println("Result real: {}", res);
}
