#include "common.hpp"
#include "parse.hpp"

#include <print>

int remove_rolls(Grid& grid)
{
    int res = 0;

    // Mark removable
    for (int x = 0; x < grid.w; x++) {
        for (int y = 0; y < grid.h; y++) {
            int i = x + y * grid.w;
            if (grid.data[i] == Cell::Empty)
                continue;
            if (count_neighbors(grid, x, y) < 4) {
                res++;
                grid.data[i] = Cell::Removable;
            }
        }
    }

    // Remove
    for (auto& c : grid.data) {
        if (c == Cell::Removable)
            c = Cell::Empty;
    }

    return res;
}

void part2(ParseType grid)
{
    int res = 0;

    while (true) {
        int removed = remove_rolls(grid);
        if (removed == 0)
            break;
        res += removed;
    }

    std::println("{}", res);
}
