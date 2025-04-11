cmake_minimum_required(VERSION 3.14)
project(hidapi-py)

if(NOT DEPS_FOLDER)
    set(DEPS_FOLDER ${CMAKE_SOURCE_DIR}/deps)
endif(NOT DEPS_FOLDER)

# Enable C++14
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

# Find pybind11 (You can use FetchContent or add_subdirectory if you include it manually)
set(PYBIND11_PYTHON_VERSION 3.11)
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    SOURCE_DIR "${DEPS_FOLDER}/pybind11"
    GIT_TAG v2.13.6
)
FetchContent_MakeAvailable(pybind11)
include_directories(${DEPS_FOLDER}/pybind11/include)

set(SOURCES
    src/bindings.cpp
)

pybind11_add_module(hidapi-py ${SOURCES})

if(WIN32)
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(ARCH_DIR "x64")
    else()
        set(ARCH_DIR "x86")
    endif()

    set(HIDAPI_ROOT "${DEPS_FOLDER}/hidapi-win")
    set(HIDAPI_INCLUDE_DIR "${HIDAPI_ROOT}/include")
    set(HIDAPI_ARCH "${HIDAPI_ROOT}/${ARCH_DIR}")
    set(HIDAPI_LIBRARY "${HIDAPI_ARCH}/hidapi.lib")
    set(HIDAPI_DLL "${HIDAPI_ARCH}/hidapi.dll")

    message(STATUS "Building for architecture: ${ARCH_DIR}")
    message(STATUS "Using HIDAPI from: ${HIDAPI_ARCH}")

    # Copy DLL to output directory
    add_custom_command(TARGET hidapi-py POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${HIDAPI_DLL}"
        $<TARGET_FILE_DIR:hidapi-py>
        COMMENT "Copying hidapi.dll to output directory"
    )
elseif(APPLE)
    if(NOT HIDAPI_ROOT)
        message(FATAL_ERROR "Please set HIDAPI_ROOT to the path where HIDAPI is installed (e.g., /opt/homebrew)")
    endif()

    set(HIDAPI_INCLUDE_DIR "${HIDAPI_ROOT}/include")
    set(HIDAPI_LIBRARY_DIR "${HIDAPI_ROOT}/lib")

    find_path(HIDAPI_INCLUDE_DIR NAMES hidapi/hidapi.h PATHS ${HIDAPI_INCLUDE_DIR} REQUIRED)
    find_library(HIDAPI_LIBRARY NAMES hidapi PATHS ${HIDAPI_LIBRARY_DIR} REQUIRED)
else()
    find_library(HIDAPI_LIBRARY NAMES hidapi-hidraw hidapi-libusb hidapi)
endif()

message(STATUS "Using HIDAPI from: ${HIDAPI_INCLUDE_DIR}")
set_target_properties(hidapi-py PROPERTIES OUTPUT_NAME "hidapi_py")
target_include_directories(hidapi-py PRIVATE ${CMAKE_SOURCE_DIR}/includes)
target_include_directories(hidapi-py PRIVATE ${HIDAPI_INCLUDE_DIR})
target_link_libraries(hidapi-py PRIVATE ${HIDAPI_LIBRARY})

SET(COPY_TO_PATH ${CMAKE_SOURCE_DIR}/../src/dualsense_controller/core/hidapi)

if(WIN32)
    add_custom_command(TARGET hidapi-py POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${HIDAPI_DLL}"
        ${COPY_TO_PATH}
        COMMENT "Copying HIDAPI DLL to output directory"
    )
endif()

add_custom_command(TARGET hidapi-py POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "Listing build output:"
    COMMAND ${CMAKE_COMMAND} -E chdir $<TARGET_FILE_DIR:hidapi-py> ls -l
)

add_custom_command(TARGET hidapi-py POST_BUILD
    VERBATIM COMMAND python3 -c "import os; print(os.getcwd()) ;" || (exit 0)
    WORKING_DIRECTORY $<TARGET_FILE_DIR:hidapi-py>
    COMMENT "Creating stubs for hidapi-py"
)

add_custom_command(TARGET hidapi-py POST_BUILD
    VERBATIM COMMAND python3 -c "import os; import sys; sys.path.insert(1, os.getcwd()) ; from pybind11_stubgen import main; import hidapi_py; sys.argv[0] = 'pybind11-stubgen'; sys.argv.append('--ignore-all-errors') ; sys.argv.append('-o') ; sys.argv.append('.') ; sys.argv.append('hidapi_py') ; main() " ||(exit 0)
    WORKING_DIRECTORY $<TARGET_FILE_DIR:hidapi-py>
    COMMENT "Creating stubs for hidapi-py"
)