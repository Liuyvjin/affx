cmake_minimum_required(VERSION 2.8.12)
project(Pyaffx)

find_package(Eigen3 REQUIRED)

add_subdirectory(pybind11)
pybind11_add_module(affx src/pyaffx.cpp)
target_link_libraries(affx PUBLIC Eigen3::Eigen)
target_include_directories(affx PUBLIC ./include)

# install to base_dir/pyaffx/
set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}")
install(TARGETS affx DESTINATION pyaffx)
