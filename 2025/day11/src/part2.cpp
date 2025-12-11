#include "parse.hpp"

#include <print>
#include <tuple>

using Cache = std::map<std::tuple<Name, bool, bool>, long>;

long traverse_devices(
    const ParseType& d, Name current, bool dac_visited, bool fft_visited, Cache& c)
{
    long res { 0 };

    auto k = std::tie(current, dac_visited, fft_visited);
    if (c.contains(k)) {
        return c.at(k);
    }

    if (current == out) {
        return (dac_visited && fft_visited) ? 1 : 0;
    }

    for (auto out : d.at(current)) {
        res += traverse_devices(d, out, out == dac || dac_visited, out == fft || fft_visited, c);
    }

    c.insert({ k, res });
    return res;
}

void part2(ParseType d)
{
    Cache c;
    std::println("{}", traverse_devices(d, svr, false, false, c));
}
