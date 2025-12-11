#ifndef INPUT_HPP_INCLUDED
#define INPUT_HPP_INCLUDED

#include <array>
#include <string_view>

static constexpr auto raw_real_input = std::to_array<char>({
#include "real_input.h"
});
static constexpr std::string_view real_input { raw_real_input };

#ifdef SPLIT_TEST
static constexpr auto raw_test_input1 = std::to_array<char>({
#include "test_input1.h"
});
static constexpr std::string_view test_input1 { raw_test_input1 };

static constexpr auto raw_test_input2 = std::to_array<char>({
#include "test_input2.h"
});
static constexpr std::string_view test_input2 { raw_test_input2 };
#else
static constexpr auto             raw_test_input = std::to_array<char>({
#include "test_input.h"
});
static constexpr std::string_view test_input1 { raw_test_input };
static constexpr std::string_view test_input2 { raw_test_input };
#endif

#endif // ifndef INPUT_HPP_INCLUDED
