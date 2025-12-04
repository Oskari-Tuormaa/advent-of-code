#include "parse.hpp"

#include <span>

inline int count_digits(long number)
{
    if (number == 0)
        return 0;
    return 1 + count_digits(number / 10);
}

template <typename Func>
long long sum_valid_ids(const Range& range, Func& predicate)
{
    long long res = 0;

    for (long i = range.start; i < range.end + 1; i++) {
        if (predicate(i)) {
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
