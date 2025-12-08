#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <ranges>
#include <sstream>
#include <string_view>
#include <tuple>
#include <vector>

struct Pos
{
    long x, y, z;
};

inline bool operator==(const Pos& lhs, const Pos& rhs)
{
    return lhs.x == rhs.x && lhs.y == rhs.y && lhs.z == rhs.z;
}

inline bool operator<(const Pos& p1, const Pos& p2)
{
    return std::tie(p1.x, p1.y, p1.z) < std::tie(p2.x, p2.y, p2.z);
}

using ParseType = std::vector<Pos>;

inline ParseType parse(std::string_view data)
{
    ParseType res;

    for (auto line : data | std::views::take(data.size() - 1) | std::views::split('\n')) {
        auto              l = std::string_view(line);
        std::stringstream ss { std::string(l) };

        Pos p;
        ss >> p.x;
        ss.ignore(); // skip ,
        ss >> p.y;
        ss.ignore(); // skip ,
        ss >> p.z;

        res.emplace_back(p);
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
