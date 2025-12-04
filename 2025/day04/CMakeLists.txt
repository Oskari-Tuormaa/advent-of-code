get_filename_component(DAY ${CMAKE_CURRENT_SOURCE_DIR} NAME)

file(GLOB SOURCES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "src/*.cpp")

add_executable(${DAY} ${SOURCES})
target_compile_definitions(${DAY} PRIVATE DAY="${DAY}")
target_link_libraries(${DAY} PRIVATE common)
target_include_directories(${DAY} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src ${CMAKE_CURRENT_BINARY_DIR})

embed_txt_file(${DAY} "src/test_input.txt")
embed_txt_file(${DAY} "src/real_input.txt")
