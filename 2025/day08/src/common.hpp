#ifndef COMMON_HPP_INCLUDED
#define COMMON_HPP_INCLUDED

#include "parse.hpp"

#include <algorithm>
#include <cmath>
#include <generator>

struct Connection
{
    Pos p1, p2;

    long dist() const
    {
        long dx = p2.x - p1.x;
        long dy = p2.y - p1.y;
        long dz = p2.z - p1.z;
        return std::sqrt(dx * dx + dy * dy + dz * dz);
    }
};

inline std::generator<Connection> get_closest_connections(std::span<Pos> boxes)
{
    std::vector<Connection> conns;
    conns.reserve(boxes.size() * boxes.size());

    for (auto [i, p1] : boxes | std::views::enumerate) {
        for (auto p2 : boxes | std::views::drop(i + 1)) {
            if (p1 == p2)
                continue;
            conns.emplace_back(p1, p2);
        }
    }

    std::ranges::sort(conns, [](auto& x, auto& y) { return x.dist() < y.dist(); });
    for (auto& conn : conns) {
        co_yield conn;
    }
}

#endif // ifndef COMMON_HPP_INCLUDED
