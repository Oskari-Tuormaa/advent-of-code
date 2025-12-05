#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <charconv>
#include <string_view>
#include <vector>

enum class Dir
{
    Left,
    Right,
};

struct Move
{
    Dir dir;
    int steps;
};

using ParseType = std::vector<Move>;

inline std::vector<Move> parse(std::string_view data)
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

#endif // ifndef PARSE_HPP_INCLUDED
