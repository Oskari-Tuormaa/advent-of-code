#ifndef COMMON_HPP_INCLUDED
#define COMMON_HPP_INCLUDED

#include <algorithm>
#include <cmath>
#include <span>

using Pack = std::span<const int>;

inline long largest_joltage(Pack pack, int n_batteries)
{
    if (n_batteries == 0) {
        return 0;
    }

    int  max     = std::ranges::max(pack.subspan(0, pack.size() - n_batteries + 1));
    auto max_pos = std::ranges::find(pack, max);

    return max * std::pow(10, n_batteries - 1)
        + largest_joltage(Pack { max_pos + 1, pack.end() }, n_batteries - 1);
}

template <typename Range, typename Func>
long total_joltage(const Range& packs, Func&& joltage_func)
{
    long joltage = 0;
    for (const auto& pack : packs) {
        joltage += joltage_func(pack);
    }
    return joltage;
}

#endif // ifndef COMMON_HPP_INCLUDED
