#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <string_view>
#include <vector>

using ParseType = std::vector<std::vector<int>>;

inline ParseType parse(std::string_view data)
{
    ParseType   res;
    auto        rest = data;
    std::size_t nl;

    while (nl = rest.find('\n'), nl != std::string_view::npos) {
        auto line = rest.substr(0, nl);
        rest      = rest.substr(nl + 1);

        std::vector<int> d_line {};
        for (auto ch : line) {
            d_line.push_back((int)ch - '0');
        }
        res.push_back(d_line);
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
