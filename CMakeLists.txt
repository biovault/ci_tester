cmake_minimum_required(VERSION 3.21)

# set the project name and version
project(cross VERSION 1.0 LANGUAGES CXX)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Log build architecture
execute_process(COMMAND uname -m COMMAND tr -d '\n' OUTPUT_VARIABLE ARCHITECTURE)
message(STATUS "Build architecture detected ${ARCHITECTURE}")

# Nedd OpenMP_ROOT on macos
find_package(OpenMP COMPONENTS CXX REQUIRED)
# add the executable and include link OpenMP
add_executable(${PROJECT_NAME} src/main.cpp)
target_link_libraries(${PROJECT_NAME} PUBLIC OpenMP::OpenMP_CXX)
target_include_directories(${PROJECT_NAME} PUBLIC OpenMP::OpenMP_CXX)

if(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        BUNDLE True
        MACOSX_BUNDLE_GUI_IDENTIFIER "com.biovault.${PROJECT_NAME}" 
        MACOSX_BUNDLE_BUNDLE_NAME ${PROJECT_NAME}
        MACOSX_BUNDLE_BUNDLE_VERSION "0.1"
        MACOSX_BUNDLE_SHORT_VERSION_STRING "0.1"
    )    
endif()

if(APPLE)
    INSTALL(TARGETS ${PROJECT_NAME} 
        RUNTIME DESTINATION bin COMPONENT MACOS_BUNDLE
        BUNDLE DESTINATION . COMPONENT MACOS_BUNDLE
    )
endif()


