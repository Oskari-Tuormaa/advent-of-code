#include "common.hpp"
#include "parse.hpp"

#include <cmath>
#include <print>

bool is_repeating(long number, int n_digits, int period)
{
    if (n_digits % period != 0)
        return false;

    long divisor = std::pow(10, period);
    long pattern = number % divisor;
    number /= divisor;
    while (number != 0) {
        if (number % divisor != pattern)
            return false;
        number /= divisor;
    }
    return true;
}

bool is_valid2(long number)
{
    int n_digits = count_digits(number);
    for (int i = n_digits / 2; i >= 1; i--) {
        if (is_repeating(number, n_digits, i))
            return true;
    }
    return false;
}

void part2(ParseType d)
{
    std::println("{}", sum_valid_ids(d, is_valid2));
}
