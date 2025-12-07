#include "parse.hpp"

#include <map>
#include <optional>
#include <print>

static std::map<Pos, long> cache {};

std::optional<Pos> shoot_beam(int h, Pos p, std::set<Pos> spl)
{
    while (p.y < h) {
        if (spl.contains(p)) {
            return p;
        }
        p.y++;
    }
    return {};
}

long walk(int h, Pos p, std::set<Pos> spl)
{
    if (cache.contains(p)) {
        return cache[p];
    }

    auto sp = shoot_beam(h, p, spl);
    if (!sp) {
        return 1;
    }

    long res = 0;
    res += walk(h, { sp->x + 1, sp->y }, spl);
    res += walk(h, { sp->x - 1, sp->y }, spl);
    cache.insert({ p, res });
    return res;
}

void part2(ParseType d)
{
    auto& [w, h, splitters, initial_beam] = d;
    std::println("{}", walk(h, initial_beam, splitters));
}
