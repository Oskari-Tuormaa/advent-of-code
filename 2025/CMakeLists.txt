cmake_minimum_required(VERSION 3.22)
project(AdventOfCode2025 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)
set(CMAKE_BUILD_TYPE Debug)

add_subdirectory(common)

file(GLOB DAYS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "day*")

foreach(DAY ${DAYS})
    add_subdirectory(${DAY})
endforeach()
