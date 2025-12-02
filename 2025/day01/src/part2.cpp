#include "ansi.hpp"
#include "input.hpp"

#include <print>

int calculate_password_0x434C49434B(std::span<const Move> moves)
{
    int res  = 0;
    int dial = 50;

    for (auto [dir, len] : moves) {
        for (int i = 0; i < len; i++) {
            dial = (dir == Dir::RIGHT ? dial + 1 : dial - 1) % 100;
            if (dial == 0)
                res++;
        }
    }

    return res;
}

void part2()
{
    std::println(PURPLE BOLD "### Part 2 ###" RESET);
    int res;

    res = calculate_password_0x434C49434B(test_input);
    std::println("Result test: {}", res);

    res = calculate_password_0x434C49434B(real_input);
    std::println("Result real: {}", res);
}
