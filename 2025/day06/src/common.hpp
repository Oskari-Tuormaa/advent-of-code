#ifndef COMMON_HPP_INCLUDED
#define COMMON_HPP_INCLUDED

#include <regex>
#include <string_view>

inline long parse_int(std::string_view vw)
{
    long       v;
    std::regex num_regex { "\\d+" };
    auto       begin = std::cregex_iterator(vw.begin(), vw.end(), num_regex);
    auto       first = begin->str();
    std::from_chars(first.data(), first.data() + first.size(), v);
    return v;
}

#endif // ifndef COMMON_HPP_INCLUDED
