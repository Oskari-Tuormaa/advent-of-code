#include "input.hpp"

#include <print>
#include <span>

int calculate_password(std::span<const Move> moves)
{
    int res  = 0;
    int dial = 50;

    for (auto [dir, len] : moves) {
        dial = (dir == Dir::LEFT ? dial+len : dial-len) % 100;
        if (dial == 0)
            res++;
    }

    return res;
}

int calculate_password2(std::span<const Move> moves)
{
    int res  = 0;
    int dial = 50;

    for (auto [dir, len] : moves) {
        for (int i = 0; i < len; i++) {
            dial = (dir == Dir::RIGHT ? dial+1 : dial-1) % 100;
            if (dial == 0) res++;
        }
    }

    return res;
}

int part1()
{
    int res;
    std::println("## Part1");

    res = calculate_password(test_input);
    std::println("Result test: {}", res);

    res = calculate_password(real_input);
    std::println("Result test: {}", res);

    return 0;
}

int part2()
{
    int res;
    std::println("## Part2");

    res = calculate_password2(test_input);
    std::println("Result test: {}", res);

    res = calculate_password2(real_input);
    std::println("Result test: {}", res);

    return 0;
}

int main()
{
    std::println("# Day 01");

    part1();
    part2();

    return 0;
}
