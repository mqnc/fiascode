
cmake_minimum_required(VERSION 3.11.0)
project (hello)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

find_package (Eigen3 3.3 REQUIRED NO_MODULE)
find_package (Boost 1.66.0 REQUIRED COMPONENTS system filesystem regex)

add_executable(hello main.cpp)

target_link_libraries (hello Eigen3::Eigen ${Boost_LIBRARIES})

