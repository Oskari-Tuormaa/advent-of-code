#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <vector>

struct Range
{
    long start;
    long end;
};

using ParseType = std::vector<Range>;

#endif // ifndef PARSE_HPP_INCLUDED
