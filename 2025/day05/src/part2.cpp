#include "parse.hpp"

#include <algorithm>
#include <cstdio>
#include <functional>
#include <print>

using namespace std::placeholders;

bool do_ranges_overlap(Range r1, Range r2)
{
    return (r2.start <= r1.end) && (r1.start <= r2.end);
}

Range combine_ranges(Range r1, Range r2)
{
    return { .start = std::min(r1.start, r2.start), .end = std::max(r1.end, r2.end) };
}

void emplace_or_combine(std::vector<Range>& ranges, Range r)
{
    auto overlap = std::ranges::find_if(ranges, std::bind(do_ranges_overlap, _1, r));
    if (overlap != ranges.end()) {
        Range new_r = combine_ranges(*overlap, r);
        ranges.erase(overlap);
        emplace_or_combine(ranges, new_r);
    } else {
        ranges.emplace_back(r);
    }
}

void part2(ParseType d)
{
    long               res = 0;
    std::vector<Range> fresh_ids {};
    auto& [ranges, ingredients] = d;

    // Combine overlapping ranges
    for (auto r : ranges) {
        emplace_or_combine(fresh_ids, r);
    }

    // Count valid IDs
    for (auto r : fresh_ids) {
        res += r.end - r.start + 1;
    }

    std::println("{}", res);
}
