add_library(common INTERFACE)
target_sources(common PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp)
target_include_directories(common INTERFACE .)
