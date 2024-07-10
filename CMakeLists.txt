cmake_minimum_required(VERSION 3.27)

# set the project name and version
project(cross VERSION 1.0 LANGUAGES CXX)

# For print variables
include(${CMAKE_CURRENT_SOURCE_DIR}/src/cmake/DebugHelpers.cmake)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Log build architecture
execute_process(COMMAND uname -m COMMAND tr -d '\n' OUTPUT_VARIABLE ARCHITECTURE)
message(STATUS "Build host architecture detected ${ARCHITECTURE}")

# Need OpenMP_ROOT on macos
find_package(OpenMP COMPONENTS CXX REQUIRED)
# add the executable and include link OpenMP
add_executable(${PROJECT_NAME} src/main.cpp)

if (APPLE AND BUILD_MACOS_UNIVERSAL)
    set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64")
endif()

print_all_variables()
target_link_libraries(${PROJECT_NAME} PUBLIC ${OpenMP_CXX_LIBRARIES})
target_include_directories(${PROJECT_NAME} PUBLIC ${OpenMP_CXX_INCLUDE_DIRS})
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")

if(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_BUNDLE TRUE    
    )
    set_target_properties(${PROJECT_NAME} PROPERTIES
        XCODE_ATTRIBUTE_LD_RUNPATH_SEARCH_PATHS "@executable_path/../Frameworks")

    set(MACOSX_BUNDLE_BUNDLE_NAME ${PROJECT_NAME})
    set(MACOSX_BUNDLE_BUNDLE_VERSION "0.1")
    set(MACOSX_BUNDLE_BUNDLE_SHORT_VERSION_STRING ${BUNDLE_VERSION})
    set(MACOSX_BUNDLE_BUNDLE_LONG_VERSION_STRING ${BUNDLE_VERSION})
    set(MACOSX_BUNDLE_GUI_IDENTIFIER "com.biovault.${PROJECT_NAME}" )
 
    set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

endif()

if(APPLE)
    INSTALL(TARGETS ${PROJECT_NAME}
        BUNDLE DESTINATION . COMPONENT MACOS_BUNDLE
        RUNTIME DESTINATION bin COMPONENT MACOS_BUNDLE
    )

    INSTALL(FILES ${OpenMP_CXX_LIBRARIES}
        DESTINATION ./cross.app/Contents/Frameworks COMPONENT MACOS_BUNDLE
    )

endif()


