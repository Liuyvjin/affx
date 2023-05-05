cmake_minimum_required(VERSION 2.8.12)
project(PyAffx)

find_package(Eigen3 REQUIRED)

add_subdirectory(pybind11)
pybind11_add_module(pyaffx src/pyaffx.cpp)
target_link_libraries(pyaffx PUBLIC Eigen3::Eigen)
target_include_directories(pyaffx PUBLIC ./include)