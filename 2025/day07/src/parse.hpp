#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <set>
#include <string_view>
#include <utility>

struct Pos
{
    int x, y;

    bool operator<(const Pos& rhs) const
    {
        return std::pair { x, y } < std::pair { rhs.x, rhs.y };
    }
};

struct ParseType
{
    int           w, h;
    std::set<Pos> splitters;
    Pos           initial_beam;
};

inline ParseType parse(std::string_view data)
{
    ParseType res;

    int         y = 0;
    std::size_t nl;
    auto        rest = data;
    while (nl = rest.find('\n'), nl != std::string_view::npos) {
        auto line = rest.substr(0, nl);
        rest      = rest.substr(nl + 1);

        int x = 0;
        for (auto ch : line) {

            if (ch == '^') {
                res.splitters.insert({ x, y });
            } else if (ch == 'S') {
                res.initial_beam = { x, y };
            }

            x++;
        }
        res.w = x;

        y++;
    }
    res.h = y;

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
