#include "ansi.hpp"
#include "input.hpp"
#include "parse.hpp"

#include <chrono>
#include <print>
#include <ratio>

extern ParseType parse(std::string_view);
extern void      part1(ParseType);
extern void      part2(ParseType);

template <typename Func>
void measure_ms(Func&& f)
{
    auto t0 = std::chrono::high_resolution_clock::now();
    f();
    auto   t1 = std::chrono::high_resolution_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::println(GREY ITALIC "took {:.3f} ms" RESET, ms);
}

int main()
{
    std::println(GREEN BOLD "===== " DAY " =====" RESET);

    {
        std::println("\n" PURPLE "### Part 1 ###" RESET);
        std::println(CYAN ITALIC "Test:" RESET);
        part1(parse(test_input));

        std::println(CYAN ITALIC "Real:" RESET);
        auto d = parse(real_input);
        measure_ms([&d] { part1(d); });
    }

    {
        std::println("\n" PURPLE "### Part 2 ###" RESET);
        std::println(CYAN ITALIC "Test:" RESET);
        part2(parse(test_input));

        std::println(CYAN ITALIC "Real:" RESET);
        auto d = parse(real_input);
        measure_ms([&d] { part2(d); });
    }
}
