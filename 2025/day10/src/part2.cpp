#include "common.hpp"
#include "parse.hpp"

#include <algorithm>
#include <generator>
#include <optional>
#include <print>
#include <ranges>

std::vector<int> press_button(const std::vector<int>& button, std::vector<int> joltages)
{
    for (auto i : button) {
        joltages[i]++;
    }
    return joltages;
}

std::generator<std::optional<long>> solve_machine_joltage_iterate(
    const Machine& m, std::vector<int> joltages, long presses = 0)
{
    bool equal = true;
    for (auto [j1, j2] : std::views::zip(m.joltage_requirements, joltages)) {
        if (j1 < j2) {
            co_return;
        }
        if (j1 != j2) {
            equal = false;
            break;
        }
    }

    if (equal) {
        co_yield presses;
    }
    co_yield {};

    std::vector<decltype(solve_machine_joltage_iterate(m, {}))>         generators;
    std::vector<decltype(solve_machine_joltage_iterate(m, {}).begin())> iterators;

    for (const auto& [i, b] : m.buttons | std::views::enumerate) {
        generators.emplace_back(
            solve_machine_joltage_iterate(m, press_button(b, joltages), presses + 1));
        iterators.emplace_back(generators[i].begin());
        co_yield {};
    }

    decltype(solve_machine_joltage_iterate(m, {}).end()) end;
    while (true) {
        for (auto& it : iterators) {
            if (it == end) {
                continue;
            }
            co_yield *it;
            it++;
        }
    }
}

long solve_machine_joltage(const Machine& m)
{
    std::vector<int> joltages;
    joltages.resize(m.joltage_requirements.size());
    for (auto r : solve_machine_joltage_iterate(m, joltages)) {
        if (r) {
            std::println("sub result: {}", *r);
            return *r;
        }
    }
    return 0;
}

void part2(ParseType d)
{
    // long res = 0;
    // for (const Machine& m : d) {
    //     res += solve_machine_joltage(m);
    // }
    // std::println("{}", res);
}
