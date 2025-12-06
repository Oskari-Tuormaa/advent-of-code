#include "common.hpp"
#include "parse.hpp"

#include <print>

std::vector<std::string> transpose(std::vector<std::string> inp)
{
    std::vector<std::string> res {};

    for (int i = 0; i < inp[0].size(); i++) {
        std::string l;
        for (int j = 0; j < inp.size(); j++) {
            l.push_back(inp[j][i]);
        }
        res.emplace_back(l);
    }

    return res;
}

long collapse_column2(Problem& column)
{
    long res = column.op == Operator::Add ? 0 : 1;

    for (auto n : transpose(column.numbers)) {
        long np = parse_int(n);
        if (column.op == Operator::Add) {
            res += np;
        } else {
            res *= np;
        }
    }

    return res;
}

void part2(ParseType d)
{
    long res = 0;

    for (auto& p : d) {
        res += collapse_column2(p);
    }

    std::println("{}", res);
}
