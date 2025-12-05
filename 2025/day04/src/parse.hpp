#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <string_view>
#include <vector>

enum class Cell
{
    Empty,
    Removable,
    Roll,
};

struct Grid
{
    int               w, h;
    std::vector<Cell> data;
};

using ParseType = Grid;

inline ParseType parse(std::string_view data)
{
    ParseType res;

    res.w = std::ranges::find(data, '\n') - std::begin(data);
    res.h = (data.size() - 1) / res.w;

    for (auto ch : data) {
        if (ch != '.' && ch != '@')
            continue;

        res.data.push_back(ch == '.' ? Cell::Empty : Cell::Roll);
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
