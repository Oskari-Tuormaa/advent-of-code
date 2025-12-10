#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <ranges>
#include <sstream>
#include <string_view>
#include <vector>

using Pos       = std::pair<long, long>;
using ParseType = std::vector<Pos>;

inline ParseType parse(std::string_view data)
{
    ParseType res;

    for (auto l : data | std::views::split('\n')) {
        std::string_view  line { l };
        std::stringstream ss { std::string { line } };
        long              x, y;
        ss >> x;
        ss.ignore();
        ss >> y;
        res.emplace_back(std::tie(x, y));
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
