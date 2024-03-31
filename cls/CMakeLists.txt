cmake_minimum_required(VERSION 3.15)
project(DEPLOY)

set(CMAKE_CXX_STANDARD 20)
find_package(OpenCV REQUIRED)
find_package(CUDA REQUIRED)

add_definitions(-D WITH_CUDA=ON)

include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(DEPLOY-cls predict.cpp)

target_link_libraries(DEPLOY-cls ${OpenCV_LIBS})
target_link_libraries(DEPLOY-cls ${CUDA_LIBRARIES})
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)