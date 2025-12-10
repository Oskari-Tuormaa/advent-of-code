#include "parse.hpp"

#include <algorithm>
#include <generator>
#include <map>
#include <print>

using Line      = std::pair<Pos, Pos>;
using Rectangle = std::pair<Pos, Pos>;

static std::map<Pos, bool> cache {};

bool is_point_within(Pos p, Line l)
{
    auto [p1, p2] = l;
    auto [x1, y1] = p1;
    auto [x2, y2] = p2;

    auto [px, py] = p;

    return y1 == y2 && px <= std::max(x1, x2) && px >= std::min(x1, x2);
}

bool is_inner(Pos p, const ParseType d)
{
    if (cache.contains(p)) {
        return cache[p];
    }

    auto Fun = [p](std::pair<Pos, Pos> l) { return is_point_within(p, l); };

    auto [x, y] = p;

    int above = 0, below = 0;
    for (auto l : d | std::views::adjacent<2> | std::views::filter(Fun)) {
        auto [p1, p2] = l;
        auto [x1, y1] = p1;

        if (y1 > y) {
            above++;
        } else if (y1 < y) {
            below++;
        }
    }

    cache.insert({ p, !((above % 2 == 0) && (below % 2 == 0)) });
    return cache[p];
}

bool is_valid(Rectangle r, const ParseType d)
{
    auto [p1, p2] = r;
    auto [x1, y1] = p1;
    auto [x2, y2] = p2;

    if (x1 == x2 || y1 == y2)
        return false;

    auto minx = std::min(x1, x2);
    auto miny = std::min(y1, y2);
    auto maxx = std::max(x1, x2);
    auto maxy = std::max(y1, y2);

    std::println("{},{} - {},{}", x1, y1, x2, y2);

    for (auto x = minx; x <= maxx; x++) {
        std::println("{}", x);
        for (auto y = miny; y <= maxy; y++) {
            if (!is_inner({ x, y }, d))
                return false;
        }
    }
    return true;
}

long area(Rectangle r)
{
    auto [p1, p2] = r;
    auto [x1, y1] = p1;
    auto [x2, y2] = p2;
    auto dx       = std::abs(x2 - x1) + 1;
    auto dy       = std::abs(y2 - y1) + 1;
    return dx * dy;
}

std::generator<Rectangle> iterate_largest(ParseType d)
{
    std::vector<Rectangle> rects;

    for (auto [i, p1] : d | std::views::enumerate) {
        for (auto p2 : d | std::views::drop(i + 1)) {
            rects.emplace_back(p1, p2);
        }
    }

    std::ranges::sort(rects, [](Rectangle& r1, Rectangle& r2) { return area(r2) < area(r1); });

    std::println("Sorted! {} rects", rects.size());
    for (auto [i, r] : rects | std::views::enumerate) {
        co_yield r;

        std::println("{}/{}", i, rects.size());
    }
}

void part2(ParseType d)
{
    for (auto r : iterate_largest(d) | std::views::drop(22247)) {
        auto [p1, p2] = r;
        auto [x1, y1] = p1;
        auto [x2, y2] = p2;

        if (is_valid(r, d)) {
            std::println("{}", area(r));
            break;
        }
    }
}
