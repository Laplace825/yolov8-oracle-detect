cmake_minimum_required(VERSION 3.15)
project(DEPLOY)

set(CMAKE_CXX_STANDARD 20)
find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(DEPLOY predict.cpp inference.cpp)

target_link_libraries(DEPLOY ${OpenCV_LIBS})
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)