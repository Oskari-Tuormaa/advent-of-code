#include "ansi.hpp"
#include "common.hpp"
#include "input.hpp"

#include <cmath>
#include <print>

bool is_valid1(long number)
{
    int n_digits = count_digits(number);
    if (n_digits % 2 != 0) {
        return false;
    }

    long divisor = std::pow(10, n_digits / 2);
    long upper   = number / divisor;
    long lower   = number % divisor;
    return upper == lower;
}

void part1()
{
    std::println(PURPLE "### Part 1 ###" RESET);
    std::println("Result test: {}", sum_valid_ids(test_input, is_valid1));
    std::println("Result real: {}", sum_valid_ids(real_input, is_valid1));
}
