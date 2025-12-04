#ifndef INPUT_HPP_INCLUDED
#define INPUT_HPP_INCLUDED

#include <algorithm>
#include <array>
#include <span>
#include <vector>

static constexpr auto test_input = std::to_array<char>({
#include "test_input.h"
});

static constexpr auto real_input = std::to_array<char>({
#include "real_input.h"
});

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

inline Grid parse_input(std::span<const char> input)
{
    int               w, h;
    std::vector<Cell> data;

    w = std::ranges::find(input, '\n') - std::begin(input);
    h = (input.size() - 1) / w;

    for (auto ch : input) {
        if (ch != '.' && ch != '@')
            continue;

        data.push_back(ch == '.' ? Cell::Empty : Cell::Roll);
    }

    return Grid { .w = w, .h = h, .data = std::move(data) };
}

#endif // ifndef INPUT_HPP_INCLUDED
