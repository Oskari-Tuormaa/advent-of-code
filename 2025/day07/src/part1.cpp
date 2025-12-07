#include "parse.hpp"

#include <print>
#include <queue>

void part1(ParseType d)
{
    int res                               = 0;
    auto& [w, h, splitters, initial_beam] = d;
    std::queue<Pos> beams_to_check {};
    std::set<Pos>   beam_positions {};

    beams_to_check.push(initial_beam);

    while (!beams_to_check.empty()) {
        auto nxt = beams_to_check.front();
        beams_to_check.pop();
        if (beam_positions.contains(nxt)) {
            continue;
        }

        auto p = nxt;
        while (p.y < h) {
            if (splitters.contains(p)) {
                beams_to_check.push({ p.x - 1, p.y });
                beams_to_check.push({ p.x + 1, p.y });
                res++;
                break;
            }

            if (beam_positions.contains(p)) {
                break;
            }
            beam_positions.insert(p);

            p.y++;
        }
    }

    std::println("{}", res);
}
