#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <regex>
#include <string_view>
#include <vector>

struct Range
{
    long start;
    long end;
};

using ParseType = std::vector<Range>;

inline long parse_int(std::string_view vw)
{
    long v;
    std::from_chars(vw.begin(), vw.end(), v);
    return v;
}

inline ParseType parse(std::string_view data)
{
    ParseType   res;
    auto        rest = data;
    std::size_t delim;

    std::regex range_regex { "(\\d+)-(\\d+)" };
    auto       range_begin = std::cregex_iterator { data.begin(), data.end(), range_regex };
    auto       range_end   = std::cregex_iterator {};

    for (auto it = range_begin; it != range_end; it++) {
        std::cmatch match = *it;
        res.emplace_back(parse_int(match[1].str()), parse_int(match[2].str()));
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
