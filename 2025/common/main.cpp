#include "ansi.hpp"

#include <chrono>
#include <print>
#include <ratio>

extern void part1();
extern void part2();

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

    measure_ms(part1);
    measure_ms(part2);
}
