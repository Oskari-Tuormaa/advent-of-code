#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <print>
#include <regex>
#include <string_view>
#include <vector>

struct Range
{
    long start;
    long end;
};

struct ParseType
{
    std::vector<Range> valid_ranges;
    std::vector<long>  ingredients;
};

inline long parse_int(std::string_view vw)
{
    long v;
    std::from_chars(vw.begin(), vw.end(), v);
    return v;
}

inline ParseType parse(std::string_view data)
{
    ParseType res;

    auto dnl         = data.find("\n\n");
    auto ranges      = data.substr(0, dnl);
    auto ingredients = data.substr(dnl + 2);

    std::regex           range_regex("(\\d+)-(\\d+)");
    std::cregex_iterator range_begin { ranges.begin(), ranges.end(), range_regex };
    std::cregex_iterator range_end {};
    for (auto it = range_begin; it != range_end; it++) {
        auto match = *it;
        res.valid_ranges.emplace_back(parse_int(match[1].str()), parse_int(match[2].str()));
    }

    std::regex           number_regex("\\d+");
    std::cregex_iterator number_begin { ingredients.begin(), ingredients.end(), number_regex };
    std::cregex_iterator number_end {};
    for (auto it = number_begin; it != number_end; it++) {
        auto match = *it;
        res.ingredients.push_back(parse_int(match[0].str()));
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
