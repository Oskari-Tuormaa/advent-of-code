#include "common.hpp"
#include "input.hpp"

#include <print>
#include <span>

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

int remove_until_inaccessible(Grid grid)
{
    int res = 0;

    while (true) {
        int removed = remove_rolls(grid);
        if (removed == 0)
            break;
        res += removed;
    }

    return res;
}

void part2()
{
    std::println("test_input: {}", remove_until_inaccessible(parse_input(test_input)));
    std::println("real_input: {}", remove_until_inaccessible(parse_input(real_input)));
}
