#include "common.hpp"
#include "parse.hpp"

#include <generator>
#include <optional>
#include <print>
#include <ranges>

uint16_t press_button(const std::vector<int>& button, uint16_t light_state)
{
    for (auto i : button) {
        light_state ^= 1 << i;
    }
    return light_state;
}

std::generator<std::optional<long>> solve_machine_iterate(
    const Machine& m, uint16_t light_state, long presses = 0)
{
    if (light_state == m.desired_lights) {
        co_yield presses;
    }
    co_yield {};

    std::vector<decltype(solve_machine_iterate(m, 0))>         generators;
    std::vector<decltype(solve_machine_iterate(m, 0).begin())> iterators;

    for (const auto& [i, b] : m.buttons | std::views::enumerate) {
        generators.emplace_back(
            solve_machine_iterate(m, press_button(b, light_state), presses + 1));
        iterators.emplace_back(generators[i].begin());
        co_yield *iterators[i];
    }

    std::vector<decltype(solve_machine_iterate(m, 0).end())> end;
    while (true) {
        for (auto& it : iterators) {
            it++;
            co_yield *it;
        }
    }
}

long solve_machine(const Machine& m)
{
    for (auto r : solve_machine_iterate(m, 0)) {
        if (r) {
            return *r;
        }
    }
    return 0;
}

void part1(ParseType d)
{
    long res = 0;
    for (const Machine& m : d) {
        res += solve_machine(m);
    }
    std::println("{}", res);
}
