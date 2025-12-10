#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <ranges>
#include <regex>
#include <sstream>
#include <string_view>
#include <vector>

struct Machine
{
    uint16_t                      desired_lights;
    std::vector<std::vector<int>> buttons;
    std::vector<int>              joltage_requirements;
};

using ParseType = std::vector<Machine>;

inline std::vector<int> parse_csv(std::string v)
{
    std::vector<int> nums {};

    std::stringstream rest { v };
    do {
        nums.emplace_back();
        rest >> nums.back();
    } while (rest.get() == ',');

    return nums;
}

inline Machine parse_machine(std::string_view line)
{
    Machine m;

    std::regex light_diagram_regex { "\\[([.#]+)\\]" };
    std::regex buttons_regex { "\\(((?:\\d,?)+)\\)" };
    std::regex joltage_regex { "\\{((?:\\d,?)+)\\}" };

    m.desired_lights = 0;
    for (auto [i, ch] :
        (*std::cregex_iterator { line.begin(), line.end(), light_diagram_regex })[1].str() | std::views::enumerate) {
        m.desired_lights |= (ch == '#') << i;
    }

    for (std::cregex_iterator it { line.begin(), line.end(), buttons_regex };
        it != std::cregex_iterator {}; it++) {
        auto match = *it;
        m.buttons.emplace_back(parse_csv(match[1]));
    }

    for (std::cregex_iterator it { line.begin(), line.end(), joltage_regex };
        it != std::cregex_iterator {}; it++) {
        auto match             = *it;
        m.joltage_requirements = parse_csv(match[1]);
    }

    return m;
}

inline ParseType parse(std::string_view data)
{
    ParseType res;

    for (auto l : data | std::views::take(data.length() - 1) | std::views::split('\n')) {
        res.emplace_back(parse_machine(std::string_view(l)));
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
