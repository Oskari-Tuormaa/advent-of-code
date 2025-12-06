#include "common.hpp"
#include "parse.hpp"

#include <print>

long collapse_column(Problem& column)
{
    long res = column.op == Operator::Add ? 0 : 1;

    for (auto n : column.numbers) {
        long np = parse_int(n);
        if (column.op == Operator::Add) {
            res += np;
        } else {
            res *= np;
        }
    }

    return res;
}

void part1(ParseType d)
{
    long res = 0;

    for (auto& p : d) {
        res += collapse_column(p);
    }

    std::println("{}", res);
}
