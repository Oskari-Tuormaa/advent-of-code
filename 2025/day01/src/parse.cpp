#include "parse.hpp"

#include <charconv>
#include <string_view>

std::vector<Move> parse(std::string_view data)
{
    int                      steps;
    std::vector<Move>        parsed {};
    auto                     rest = data;
    decltype(data.find('#')) nl;

    while (nl = rest.find('\n'), nl != std::string_view::npos) {
        auto line = rest.substr(0, nl);
        rest      = rest.substr(nl + 1);

        auto dist = line.substr(1);
        std::from_chars(dist.data(), dist.data() + dist.length(), steps);

        parsed.emplace_back(line[0] == 'L' ? Dir::Left : Dir::Right, steps);
    }

    return parsed;
}
