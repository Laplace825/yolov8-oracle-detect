cmake_minimum_required(VERSION 3.15)
project(DEPLOY)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_BUILD_TYPE "Release")
find_package(OpenCV REQUIRED)
set(CMAKE_CXX_COMPILE /usr/bin/g++)
set(CMAKE_C_COMPILE /usr/bin/gcc)

message(${CMAKE_CXX_COMPILE})
message(${CMAKE_C_COMPILE})
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${PROJECT_SOURCE_DIR}/include)
add_executable(DEPLOY main.cpp inference.cpp)
target_link_libraries(DEPLOY ${OpenCV_LIBS})


set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)