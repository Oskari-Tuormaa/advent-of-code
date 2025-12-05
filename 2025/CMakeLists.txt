cmake_minimum_required(VERSION 3.22)
project(AdventOfCode2025 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)
set(CMAKE_BUILD_TYPE Release)

add_subdirectory(common)

function(embed_txt_file TARGET_NAME Input_TXT_FILE)
    get_filename_component(INPUT_BASENAME ${Input_TXT_FILE} NAME_WE)
    set(Output_HPP_FILE ${CMAKE_CURRENT_BINARY_DIR}/${INPUT_BASENAME}.h)
    add_custom_command(
        OUTPUT ${Output_HPP_FILE}
        COMMAND xxd -i <${Input_TXT_FILE} > ${Output_HPP_FILE}
        DEPENDS ${Input_TXT_FILE}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Embedded ${Input_TXT_FILE} using xxd"
    )
    target_sources(${TARGET_NAME} PRIVATE ${Output_HPP_FILE})
endfunction()

file(GLOB DAYS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "day*")

foreach(DAY ${DAYS})
    add_subdirectory(${DAY})
endforeach()
