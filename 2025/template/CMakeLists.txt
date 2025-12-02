get_filename_component(DAY ${CMAKE_CURRENT_SOURCE_DIR} NAME)

file(GLOB SOURCES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "src/*.cpp")

add_executable(${DAY} ${SOURCES})
target_compile_definitions(${DAY} PRIVATE DAY="${DAY}")
target_link_libraries(${DAY} PRIVATE common)
