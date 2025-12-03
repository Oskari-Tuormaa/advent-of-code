#ifndef COMMON_HPP_INCLUDED
#define COMMON_HPP_INCLUDED

#include <span>

using Pack = std::span<const int>;

template<typename Range, typename Func>
long total_joltage(const Range &packs, Func&& joltage_func) {
    long joltage = 0;
    for (const auto& pack : packs) {
        joltage += joltage_func(pack);
    }
    return joltage;
}

#endif // ifndef COMMON_HPP_INCLUDED
