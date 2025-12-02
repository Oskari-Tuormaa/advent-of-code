#include "ansi.hpp"

#include <chrono>
#include <print>

extern void part1();
extern void part2();

int main()
{
    std::println(GREEN BOLD "===== " DAY " =====" RESET);
    std::chrono::high_resolution_clock clock {};

    {
        auto t0 = clock.now();
        part1();
        auto dt = clock.now() - t0;
        std::println(GREY ITALIC "Part 1 took {}" RESET, dt);
    }

    {
        auto t0 = clock.now();
        part2();
        auto dt = clock.now() - t0;
        std::println(GREY ITALIC "Part 2 took {}" RESET, dt);
    }

    return 0;
}
