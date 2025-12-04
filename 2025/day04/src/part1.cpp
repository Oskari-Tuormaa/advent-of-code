#include "common.hpp"
#include "parse.hpp"

#include <print>

void part1(ParseType grid)
{
    int res = 0;

    for (int x = 0; x < grid.w; x++) {
        for (int y = 0; y < grid.h; y++) {
            if (grid.data[x + y * grid.w] == Cell::Empty)
                continue;
            res += count_neighbors(grid, x, y) < 4 ? 1 : 0;
        }
    }

    std::println("{}", res);
}
