cmake_minimum_required(VERSION 3.21)

# set the project name and version
project(cross_omp VERSION 1.0 LANGUAGES CXX)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Log build architecture
execute_process(COMMAND uname -m COMMAND tr -d '\n' OUTPUT_VARIABLE ARCHITECTURE)
message(STATUS "Build architecture detected ${ARCHITECTURE}")

find_package(OpenMP COMPONENTS CXX REQUIRED)
# add the executable and include link OpenMP
add_executable(${PROJECT_NAME} src/main.cpp)
target_link_libraries(${PROJECT_NAME} PUBLIC OpenMP::OpenMP_CXX)
target_include_directories(${PROJECT_NAME} PUBLIC OpenMP::OpenMP_CXX)

