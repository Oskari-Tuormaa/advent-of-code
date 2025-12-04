#include "input.hpp"
#include "common.hpp"

#include <print>
#include <span>

int count_free_rolls(const Grid& grid)
{
    int res = 0;

    for (int x = 0; x < grid.w; x++) {
        for (int y = 0; y < grid.h; y++) {
            if (grid.data[x + y*grid.w] == Cell::Empty)
                continue;
            res += count_neighbors(grid, x, y) < 4 ? 1 : 0;
        }
    }

    return res;
}

void part1()
{
    std::println("test_input: {}", count_free_rolls(parse_input(test_input)));
    std::println("real_input: {}", count_free_rolls(parse_input(real_input)));
}
