#include "parse.hpp"

#include <string_view>

ParseType parse(std::string_view data)
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
