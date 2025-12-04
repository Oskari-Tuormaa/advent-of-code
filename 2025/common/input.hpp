#ifndef INPUT_HPP_INCLUDED
#define INPUT_HPP_INCLUDED

#include <array>
#include <string_view>

static constexpr auto raw_test_input = std::to_array<char>({
#include "test_input.h"
});

static constexpr auto raw_real_input = std::to_array<char>({
#include "real_input.h"
});

static constexpr std::string_view test_input {raw_test_input};
static constexpr std::string_view real_input {raw_real_input};

#endif // ifndef INPUT_HPP_INCLUDED
