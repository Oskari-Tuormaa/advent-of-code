#ifndef PARSE_HPP_INCLUDED
#define PARSE_HPP_INCLUDED

#include <cstdint>
#include <map>
#include <ranges>
#include <regex>
#include <set>
#include <string_view>

using Name      = uint32_t;
using ParseType = std::map<Name, std::set<Name>>;

inline constexpr uint32_t encode(std::string_view name)
{
    const uint8_t* raw = (const uint8_t*)name.data();
    return raw[0] + (raw[1] << 8) + (raw[2] << 16);
}

static uint32_t you { encode("you") };
static uint32_t out { encode("out") };

static uint32_t svr { encode("svr") };
static uint32_t dac { encode("dac") };
static uint32_t fft { encode("fft") };

inline ParseType parse(std::string_view data)
{
    ParseType res;

    std::regex name_regex { "\\w\\w\\w" };

    for (auto l : data | std::views::take(data.size() - 1) | std::views::split('\n')) {
        std::string_view line { l };

        auto spl = line.find(": ");
        auto dev = line.substr(0, spl);
        line     = line.substr(spl + 1);

        std::set<Name> outputs;
        for (std::cregex_iterator it { line.begin(), line.end(), name_regex };
            it != std::cregex_iterator {}; it++) {
            auto match = *it;
            outputs.insert(encode(match[0].str()));
        }

        res.insert({ encode(dev), outputs });
    }

    return res;
}

#endif // ifndef PARSE_HPP_INCLUDED
