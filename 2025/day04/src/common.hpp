#ifndef COMMON_HPP_INCLUDED
#define COMMON_HPP_INCLUDED

#include "parse.hpp"

inline int count_neighbors(const Grid& grid, int x, int y)
{
    int res = 0;
    int x1  = std::max(x - 1, 0);
    int x2  = std::min(x + 2, grid.w);
    int y1  = std::max(y - 1, 0);
    int y2  = std::min(y + 2, grid.h);

    for (int xx = x1; xx < x2; xx++) {
        for (int yy = y1; yy < y2; yy++) {
            if (xx == x && yy == y)
                continue;
            if (grid.data[xx + yy * grid.w] != Cell::Empty)
                res++;
        }
    }

    return res;
}

#endif // ifndef COMMON_HPP_INCLUDED
