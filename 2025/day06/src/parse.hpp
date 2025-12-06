#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <string>
#include <string_view>
#include <vector>

enum class Operator
{
    Add,
    Multiply,
};

struct Problem
{
    std::vector<std::string> numbers;
    Operator                 op;
};

using ParseType = std::vector<Problem>;

inline std::vector<std::string_view> into_lines(std::string_view data)
{
    std::vector<std::string_view> res;
    auto                          rest = data;

    std::size_t nl;
    while (nl = rest.find('\n'), nl != std::string_view::npos) {
        res.push_back(rest.substr(0, nl));
        rest = rest.substr(nl + 1);
    }

    return res;
}

inline ParseType parse(std::string_view data)
{
    ParseType res;

    auto lines = into_lines(data);

    Problem p {};
    for (std::size_t i = 0; i < lines[0].size(); i++) {
        // If all spaces = copy p to res and clear p
        bool all_spaces = true;
        for (std::size_t l = 0; l < lines.size() - 1; l++) {
            if (lines[l][i] != ' ') {
                all_spaces = false;
                break;
            }
        }
        if (all_spaces) {
            res.emplace_back(p);
            p.numbers.clear();
            continue;
        }

        // If operator not space = add operator to p
        if (lines[lines.size() - 1][i] != ' ') {
            p.op = lines[lines.size() - 1][i] == '+' ? Operator::Add : Operator::Multiply;
        }

        // Add data to p
        for (std::size_t l = 0; l < lines.size() - 1; l++) {
            if (p.numbers.size() <= l) {
                p.numbers.emplace_back();
            }
            p.numbers[l].push_back(lines[l][i]);
        }
    }
    res.emplace_back(p);

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
