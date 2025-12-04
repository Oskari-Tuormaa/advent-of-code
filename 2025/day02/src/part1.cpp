#include "common.hpp"
#include "parse.hpp"

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

void part1(ParseType d)
{
    std::println("{}", sum_valid_ids(d, is_valid1));
}
