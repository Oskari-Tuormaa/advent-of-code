#include "input.hpp"

#include <cmath>
#include <print>
#include <span>

// #define DEBUG1
// #define DEBUG

int count_digits(long number)
{
    if (number == 0)
        return 0;
    return 1 + count_digits(number / 10);
}

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

bool is_valid1(long number)
{
    int n_digits = count_digits(number);
    if (n_digits % 2 != 0) {
        return false;
    }

    long divisor = std::pow(10, n_digits / 2);
    long upper   = number / divisor;
    long lower   = number % divisor;
#ifdef DEBUG1
    std::println("{} = {}  {}", number, upper, lower);
#endif
    return upper == lower;
}

bool is_valid2(long number)
{
    int n_digits = count_digits(number);
    for (int i = 1; i <= n_digits / 2; i++) {
        if (is_repeating(number, n_digits, i))
            return true;
    }
    return false;
}

template <typename Func>
long long sum_valid_ids(const Range& range, Func& predicate)
{
    long long res = 0;
#ifdef DEBUG
    std::println("Checking range: [{}, {}]", range.start, range.end);
#endif

    for (long i = range.start; i < range.end + 1; i++) {
        if (predicate(i)) {
#ifdef DEBUG
            std::println("  > {}", i);
#endif
            res += i;
        }
    }

    return res;
}

template <typename Func>
long long sum_valid_ids(std::span<const Range> ranges, Func& predicate)
{
    long long res = 0;

    for (Range r : ranges) {
        res += sum_valid_ids(r, predicate);
    }

    return res;
}

int part1()
{
    std::println("## Part 1");
    std::println("test: {}", sum_valid_ids(test_input, is_valid1));
    std::println("real: {}", sum_valid_ids(real_input, is_valid1));

    std::println("## Part 2");
    std::println("test: {}", sum_valid_ids(test_input, is_valid2));
    std::println("real: {}", sum_valid_ids(real_input, is_valid2));
    return 0;
}

int part2()
{
    return 0;
}

int main()
{
    std::println("# Day 02");

    part1();
    part2();

    return 0;
}
