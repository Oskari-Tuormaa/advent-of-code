#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

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

#endif // ifndef PARSE_HPP_INCLUDED
