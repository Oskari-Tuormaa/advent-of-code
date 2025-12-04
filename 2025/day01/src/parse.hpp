#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

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

#endif // ifndef PARSE_HPP_INCLUDED
