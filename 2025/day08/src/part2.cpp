#include "common.hpp"
#include "parse.hpp"

#include <map>
#include <print>

void part2(ParseType d)
{
    std::map<int, int> circuit_sizes;
    std::map<Pos, int> circuits;

    for (auto [i, p] : d | std::views::enumerate) {
        circuits.insert({ p, i });
        circuit_sizes.insert({ i, 1 });
    }

    for (auto [p1, p2] : get_closest_connections(d)) {

        int c1 = circuits[p1];
        int c2 = circuits[p2];
        if (c1 == c2) {
            continue;
        }

        int& cs1 = circuit_sizes[c1];
        int& cs2 = circuit_sizes[c2];

        if ((cs1 + cs2) == d.size()) {
            std::println("{}", p1.x * p2.x);
            break;
        }

        for (auto& [p, cc] : circuits) {
            if (cc == c2) {
                cc = c1;
                cs1++;
                cs2--;
            }
        }
    }
}
