#include "common.hpp"
#include "parse.hpp"

#include <algorithm>
#include <map>
#include <print>
#include <ranges>

void part1(ParseType d)
{
    std::map<int, int> circuit_sizes;
    std::map<Pos, int> circuits;

    for (auto [i, p] : d | std::views::enumerate) {
        circuits.insert({ p, i });
        circuit_sizes.insert({ i, 1 });
    }

    for (auto [p1, p2] : get_closest_connections(d) | std::views::take(1000)) {

        int c1 = circuits[p1];
        int c2 = circuits[p2];
        if (c1 == c2) {
            continue;
        }

        int& cs1 = circuit_sizes[c1];
        int& cs2 = circuit_sizes[c2];
        for (auto& [p, cc] : circuits) {
            if (cc == c2) {
                cc = c1;
                cs1++;
                cs2--;
            }
        }
    }

    std::vector<int> sizes;
    for (auto [k, v] : circuit_sizes) {
        sizes.emplace_back(v);
    }
    std::ranges::sort(sizes, std::greater<>());

    long res = sizes[0] * sizes[1] * sizes[2];
    std::println("{}", res);
}
